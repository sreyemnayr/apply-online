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

    def test_phone(self):
        obj = factories.FamilyFactory.create(home_phone='6015550663')
        assert str(obj.home_phone) == "+16015550663", f"Should create with phone number {obj.home_phone}"


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