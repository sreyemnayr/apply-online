#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "applyonline.config")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

    try:
        from configurations.management import execute_from_command_line
        import django  # noqa
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

    if sys.argv[1] == "runserver":
        from datetime import date

        django.setup()
        call_command("migrate")
        call_command("createinitialfieldhistory")
        from django.contrib.auth import get_user_model

        User = get_user_model()
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        from tests.applyonline.factories import model_factories
        from random import randint

        school_year = model_factories.SchoolYearFactory(
            start=date(2019, 8, 7), end=date(2020, 5, 30), open=True
        )

        for n in ["bigfam", "fam2", "fam3", "fam4", "fam5", "fam6", "fam7", "fam8"]:
            u = User.objects.create_superuser(n, f"{n}@bigfam.com", n)
            parent = u.profile
            family = parent.families.first()

            p = model_factories.ParentFactory()
            family.parents.add(p)
            p = model_factories.ParentFactory()
            family.parents.add(p)

            s1 = model_factories.StudentFactory(male=True)
            family.students.add(s1)
            s2 = model_factories.StudentFactory(female=True)
            family.students.add(s2)
            s3 = model_factories.StudentFactory(female=True)
            family.students.add(s3)
            s4 = model_factories.StudentFactory()
            family.students.add(s4)

            for s in [s1, s2, s3, s4]:
                applying_for = randint(-4, 8)
                a = model_factories.ApplicationFactory.create(
                    school_year=school_year,
                    student=s,
                    applying_for=applying_for,
                    current_grade=applying_for - 1 if applying_for > -4 else None,
                )
                s.save()
                a.save()

    execute_from_command_line(sys.argv)
