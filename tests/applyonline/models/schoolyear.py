import pytest
from tests.applyonline import factories
import applyonline.models

pytestmark = pytest.mark.django_db


@pytest.mark.schoolyear
@pytest.mark.model
class TestSchoolYearModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = factories.SchoolYearFactory.create()
        assert obj.pk is not None, "Should create a new School Year instance"