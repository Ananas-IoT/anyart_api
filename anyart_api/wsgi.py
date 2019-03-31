"""
WSGI config for anyart_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from .settings import DEBUG
from django.core.wsgi import get_wsgi_application


if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anyart_api.settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anyart_api.prod_settings')


application = get_wsgi_application()
