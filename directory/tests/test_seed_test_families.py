from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from directory.models import Child, Device, Family, Parent


class SeedTestFamiliesCommandTests(TestCase):
    def test_seed_test_families_creates_reusable_directory(self):
        stdout = StringIO()

        call_command("seed_test_families", stdout=stdout)
        call_command("seed_test_families", stdout=stdout)

        self.assertEqual(Family.objects.count(), 3)
        self.assertEqual(Parent.objects.count(), 6)
        self.assertEqual(Child.objects.count(), 6)
        self.assertEqual(Device.objects.count(), 15)

        self.assertTrue(
            Device.objects.filter(
                sip_extension="2642",
                sip_username="2642",
                sip_secret="test-2642",
                assigned_family__name="Maple",
            ).exists()
        )
        self.assertTrue(
            Device.objects.filter(
                sip_extension="3552",
                assigned_child__name="Alex",
                assigned_child__family__name="River",
            ).exists()
        )
        self.assertTrue(
            Device.objects.filter(
                sip_extension="2362",
                assigned_parent__display_name="Quinn",
                assigned_parent__family__name="Cedar",
            ).exists()
        )
