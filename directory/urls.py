from django.urls import path

from . import views


app_name = "directory"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("children/new/", views.child_create, name="child_create"),
    path("children/<int:child_id>/edit/", views.child_update, name="child_update"),
    path(
        "children/<int:child_id>/blackouts/new/",
        views.blackout_create,
        name="blackout_create",
    ),
    path(
        "blackouts/<int:blackout_id>/edit/",
        views.blackout_update,
        name="blackout_update",
    ),
    path(
        "blackouts/<int:blackout_id>/deactivate/",
        views.blackout_deactivate,
        name="blackout_deactivate",
    ),
    path("contacts/new/", views.contact_create, name="contact_create"),
    path("contacts/<int:contact_id>/remove/", views.contact_delete, name="contact_delete"),
    path(
        "contact-permissions/new/",
        views.external_contact_permission_create,
        name="external_contact_permission_create",
    ),
    path(
        "contact-permissions/<int:permission_id>/revoke/",
        views.external_contact_permission_revoke,
        name="external_contact_permission_revoke",
    ),
    path(
        "family-permissions/request/",
        views.child_family_relationship_request,
        name="child_family_relationship_request",
    ),
    path(
        "family-permissions/<int:relationship_id>/approve/",
        views.child_family_relationship_approve,
        name="child_family_relationship_approve",
    ),
    path(
        "family-permissions/<int:relationship_id>/revoke/",
        views.child_family_relationship_revoke,
        name="child_family_relationship_revoke",
    ),
    path("conference-groups/new/", views.conference_group_create, name="conference_group_create"),
    path(
        "conference-groups/<int:group_id>/edit/",
        views.conference_group_update,
        name="conference_group_update",
    ),
]
