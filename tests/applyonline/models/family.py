import pytest
from tests.applyonline import factories
import applyonline.models

pytestmark = pytest.mark.django_db


@pytest.mark.family
@pytest.mark.model
class TestFamilyModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = factories.FamilyFactory.create()
        assert obj.pk is not None, "Should create a new Family instance"


@pytest.mark.parent
@pytest.mark.model
class TestParentModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = factories.ParentFactory.create()
        assert obj.pk is not None, "Should create a new Parent instance"


@pytest.mark.sibling
@pytest.mark.model
class TestSiblingModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = factories.SiblingFactory.create()
        assert obj.pk is not None, "Should create a new Sibling instance"