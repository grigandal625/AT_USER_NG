import os

import django
from django.core.asgi import get_asgi_application

from at_user_ng.core.arguments import get_args
from at_user_ng.utils.settings import get_django_settings_module

settings_module = get_django_settings_module()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
django.setup()

args = get_args()

django_application = get_asgi_application()

__all__ = ["django_application", "get_args"]
