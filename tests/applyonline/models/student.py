import pytest
from tests.applyonline import factories
import applyonline.models

pytestmark = pytest.mark.django_db


@pytest.mark.student
@pytest.mark.model
class TestStudentModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = factories.StudentFactory.create()
        assert obj.pk is not None, "Should create a new Student instance"
