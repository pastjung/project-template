from config.settings.base import *  # noqa: F403

DEBUG = False
APP_ENV = "test"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

