import os
import dj_database_url
import subprocess
import logging
import warnings
from django.utils.deprecation import RemovedInDjango30Warning
from .common import Common
import better_exceptions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SECRET_KEY", "superSecretKey")

DEBUG = True
SHELL_PLUS_PRINT_SQL = True

better_exceptions.MAX_LENGTH = None

logging.getLogger("factory").setLevel(logging.WARN)
warnings.filterwarnings(action="ignore", category=RemovedInDjango30Warning)


class Local(Common):
    DEBUG = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    # INSTALLED_APPS += ('django_nose',)
    INSTALLED_APPS += ("django_extensions",)
    INSTALLED_APPS += ("export_app",)

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    db_config = subprocess.run(["pg_tmp", "-t"], capture_output=True).stdout
    print(str(db_config))

    DATABASES = Common.DATABASES
    DATABASES["default"] = dj_database_url.config(default=db_config.decode("utf8"))

    # EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"



