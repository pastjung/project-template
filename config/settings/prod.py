import os

from django.core.exceptions import ImproperlyConfigured

from config.settings.base import *  # noqa: F403

DEBUG = False
APP_ENV = "prod"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY or SECRET_KEY == "change-me":
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be set to a real secret in production."
    )

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
