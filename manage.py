#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "applyonline.config")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

    try:
        from configurations.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    from django.core.management import call_command

    if sys.argv[1] == 'runserver':
        import django
        django.setup()
        call_command('migrate')
        call_command('createinitialfieldhistory')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin')


    execute_from_command_line(sys.argv)
