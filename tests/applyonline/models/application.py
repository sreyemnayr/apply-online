import pytest
from tests.applyonline import factories
from datetime import date

import applyonline.models

pytestmark = pytest.mark.django_db


@pytest.mark.application
@pytest.mark.model
class TestApplicationModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = factories.ApplicationFactory.create()
        assert obj.pk is not None, "Should create a new Application instance"
        assert obj.student.pk is not None, "Should create a new Student instance"

    def test_dob_conversion(self):
        school_year = factories.SchoolYearFactory.create(start=date(2018,8,1),open=True)
        student = factories.StudentFactory.create(dob=date(2016,8,1))
        obj = factories.ApplicationFactory.create(school_year=school_year, student=student)

        assert obj.student_age_months == 24, "Student should be 24 months"
        assert obj.student_age_years == 2.0, "Student should be 2.0 years"

    def test_percent_complete(self):
        obj = factories.ApplicationFactory.create()

        assert obj.percent_complete > 0, "Should not be zero"
        assert obj.percent_complete < 100, "Should not be complete"
        assert obj.complete is False, "Should not be complete"

        family = factories.FamilyFactory.create()
        obj.families.add(family)

        #obj.save()

        assert family in obj.families.all(), "Family in families?"

        assert obj.percent_complete == 100, f"Should now be complete {obj.incomplete_fields}"
        assert obj.complete is True, "Should be complete"


@pytest.mark.application
@pytest.mark.model
class TestOtherSchoolModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = factories.OtherSchoolFactory.create()
        assert obj.pk is not None, "Should create a new instance"