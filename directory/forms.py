from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import (
    AllowedChildFamilyRelationship,
    Child,
    ChildBlackoutPeriod,
    ConferenceGroup,
    ExternalContactPermission,
    ExternalPhoneNumber,
    Family,
    FamilyContact,
    Parent,
)


class ParentRegistrationForm(UserCreationForm):
    family_name = forms.CharField(max_length=200)
    display_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.CharField(max_length=32, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_family_name(self):
        family_name = self.cleaned_data["family_name"]
        if Family.objects.filter(name__iexact=family_name).exists():
            raise forms.ValidationError("A family with this name already exists.")
        return family_name

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            family = Family.objects.create(name=self.cleaned_data["family_name"])
            Parent.objects.create(
                user=user,
                family=family,
                display_name=self.cleaned_data["display_name"],
                email=self.cleaned_data["email"],
                phone=self.cleaned_data["phone"],
                is_guardian=True,
            )
        return user


class ChildForm(forms.ModelForm):
    def __init__(self, *args, family, **kwargs):
        super().__init__(*args, **kwargs)
        self.family = family

    class Meta:
        model = Child
        fields = ("name", "notes")
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def _post_clean(self):
        self.instance.family = self.family
        super()._post_clean()


class ChildBlackoutPeriodForm(forms.ModelForm):
    def __init__(self, *args, child, approved_by, **kwargs):
        super().__init__(*args, **kwargs)
        self.child = child
        self.approved_by = approved_by

    class Meta:
        model = ChildBlackoutPeriod
        fields = ("label", "day_group", "start_time", "end_time", "is_active", "notes")
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def _post_clean(self):
        self.instance.child = self.child
        self.instance.approved_by = self.approved_by
        super()._post_clean()


class FamilyContactForm(forms.Form):
    label = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=32)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def save(self, family):
        phone_number, _ = ExternalPhoneNumber.objects.get_or_create_normalized(
            self.cleaned_data["phone_number"]
        )
        contact, _ = FamilyContact.objects.update_or_create(
            family=family,
            external_phone_number=phone_number,
            defaults={
                "label": self.cleaned_data["label"],
                "notes": self.cleaned_data["notes"],
            },
        )
        return contact


class ExternalContactPermissionForm(forms.ModelForm):
    class Meta:
        model = ExternalContactPermission
        fields = ("child", "external_phone_number", "notes")
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, family, **kwargs):
        super().__init__(*args, **kwargs)
        self.family = family
        self.fields["child"].queryset = Child.objects.filter(family=family)
        self.fields["external_phone_number"].queryset = ExternalPhoneNumber.objects.filter(
            family_contacts__family=family
        ).distinct()
        self.fields["external_phone_number"].label = "Family contact number"


class ChildFamilyRelationshipRequestForm(forms.ModelForm):
    target_family_name = forms.CharField(
        max_length=200,
        label="Family name",
        help_text="Enter the family name exactly as they registered it.",
    )

    class Meta:
        model = AllowedChildFamilyRelationship
        fields = ("child", "target_family_name", "notes")
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, family, **kwargs):
        super().__init__(*args, **kwargs)
        self.family = family
        self.target_family = None
        self.fields["child"].queryset = Child.objects.filter(family=family)

    def clean_target_family_name(self):
        name = self.cleaned_data["target_family_name"].strip()
        try:
            target_family = Family.objects.get(name__iexact=name)
        except Family.DoesNotExist as exc:
            raise forms.ValidationError("No family with that exact name was found.") from exc
        if target_family == self.family:
            raise forms.ValidationError("Choose a family outside your own family.")
        self.target_family = target_family
        return name

    def clean(self):
        cleaned_data = super().clean()
        child = cleaned_data.get("child")
        if child and self.target_family:
            existing = AllowedChildFamilyRelationship.objects.filter(
                child=child,
                target_family=self.target_family,
            )
            if existing.exists():
                raise forms.ValidationError("That child already has a request for this family.")
        return cleaned_data


class ConferenceGroupForm(forms.ModelForm):
    class Meta:
        model = ConferenceGroup
        fields = ("name", "members", "is_active", "notes")
        widgets = {
            "members": forms.CheckboxSelectMultiple,
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, family, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["members"].queryset = Child.objects.filter(family=family)

    def clean_members(self):
        members = self.cleaned_data["members"]
        if members.count() < 2:
            raise forms.ValidationError("Choose at least two children.")
        return members
