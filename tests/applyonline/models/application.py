import pytest
from tests.applyonline import factories
import applyonline.models

pytestmark = pytest.mark.django_db


@pytest.mark.application
@pytest.mark.model
class TestApplicationModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = factories.ApplicationFactory.create()
        assert obj.pk == 1, "Should create a new Application instance"