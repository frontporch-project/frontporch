from unittest.mock import patch

from django.db import transaction
from django.test import TransactionTestCase, override_settings

from directory.models import ExternalPhoneNumber, Family, FamilyContact


class AsteriskAutoReloadSignalTests(TransactionTestCase):
    @override_settings(ASTERISK_AUTO_APPLY_CONFIG=True)
    @patch("directory.asterisk.autoreload.apply_asterisk_configuration")
    def test_asterisk_affecting_create_applies_configuration_after_commit(self, apply):
        Family.objects.create(name="River House")

        apply.assert_called_once_with(reload=True)

    @override_settings(ASTERISK_AUTO_APPLY_CONFIG=True)
    @patch("directory.asterisk.autoreload.apply_asterisk_configuration")
    def test_asterisk_affecting_delete_applies_configuration_after_commit(self, apply):
        with override_settings(ASTERISK_AUTO_APPLY_CONFIG=False):
            family = Family.objects.create(name="River House")

        family.delete()

        apply.assert_called_once_with(reload=True)

    @override_settings(ASTERISK_AUTO_APPLY_CONFIG=True)
    @patch("directory.asterisk.autoreload.apply_asterisk_configuration")
    def test_rolled_back_change_does_not_apply_configuration(self, apply):
        try:
            with transaction.atomic():
                Family.objects.create(name="Rolled Back House")
                raise RuntimeError("rollback")
        except RuntimeError:
            pass

        apply.assert_not_called()

    @override_settings(ASTERISK_AUTO_APPLY_CONFIG=True)
    @patch("directory.asterisk.autoreload.apply_asterisk_configuration")
    def test_non_rendered_contact_label_change_does_not_apply_configuration(self, apply):
        with override_settings(ASTERISK_AUTO_APPLY_CONFIG=False):
            family = Family.objects.create(name="River House")
            number = ExternalPhoneNumber.objects.create(normalized_number="+12125550100")

        FamilyContact.objects.create(
            family=family,
            external_phone_number=number,
            label="Grandparent",
        )

        apply.assert_not_called()
