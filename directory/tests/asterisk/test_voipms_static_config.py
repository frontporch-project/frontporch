import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase


ASTERISK_ETC = Path(settings.BASE_DIR) / "asterisk" / "etc"


class VoipMsStaticConfigTests(SimpleTestCase):
    def test_voipms_include_hooks_are_present(self):
        pjsip = (ASTERISK_ETC / "pjsip.conf").read_text(encoding="utf-8")
        extensions = (ASTERISK_ETC / "extensions.conf").read_text(encoding="utf-8")

        self.assertIn("#tryinclude pjsip_voipms.conf", pjsip)
        self.assertIn("#tryinclude extensions_voipms.conf", extensions)
        self.assertNotIn("[101](endpoint-basic)", pjsip)
        self.assertNotIn("[102](endpoint-basic)", pjsip)
        self.assertNotIn("password=101", pjsip)
        self.assertNotIn("password=102", pjsip)

    def test_voipms_example_files_define_trunk_and_inbound_context(self):
        pjsip = (ASTERISK_ETC / "pjsip_voipms.conf.example").read_text(
            encoding="utf-8"
        )
        extensions = (ASTERISK_ETC / "extensions_voipms.conf.example").read_text(
            encoding="utf-8"
        )

        self.assertIn("[voipms-endpoint]", pjsip)
        self.assertIn("[voipms-auth]", pjsip)
        self.assertIn("[voipms-registration]", pjsip)
        self.assertIn("[voipms-identify]", pjsip)
        self.assertIn("context=frontporch-public-inbound", pjsip)
        self.assertIn("server_uri=sip:VOIPMS_SERVER", pjsip)
        self.assertIn("client_uri=sip:VOIPMS_USERNAME@VOIPMS_SERVER", pjsip)
        self.assertIn("Public DID handling is generated from Django", extensions)
        self.assertIn("frontporch-public-inbound", extensions)
        self.assertNotIn("exten =>", extensions)

    def test_voipms_committed_examples_do_not_contain_real_passwords(self):
        pjsip = (ASTERISK_ETC / "pjsip_voipms.conf.example").read_text(
            encoding="utf-8"
        )

        password_assignments = re.findall(r"^password=(.+)$", pjsip, re.MULTILINE)

        self.assertEqual(password_assignments, ["VOIPMS_PASSWORD"])

    def test_ami_example_is_private_and_uses_placeholder_secret(self):
        manager = (ASTERISK_ETC / "manager.conf.example").read_text(encoding="utf-8")

        self.assertIn("enabled = yes", manager)
        self.assertIn("bindaddr = 100.64.0.10", manager)
        self.assertIn("[frontporch-reload]", manager)
        self.assertIn("secret = CHANGE_ME", manager)
        self.assertIn("read = command", manager)
        self.assertIn("write = command", manager)
        self.assertNotIn("bindaddr = 0.0.0.0", manager)
