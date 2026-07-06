from django.conf import settings
from django.db import transaction

from directory.asterisk.apply import apply_asterisk_configuration


def schedule_asterisk_configuration_apply():
    if not getattr(settings, "ASTERISK_AUTO_APPLY_CONFIG", False):
        return

    transaction.on_commit(lambda: apply_asterisk_configuration(reload=True))
