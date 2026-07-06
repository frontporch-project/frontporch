"""WSGI config for FrontPorch."""
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontporch.settings")

application = get_wsgi_application()
