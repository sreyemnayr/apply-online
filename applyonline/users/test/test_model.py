import pytest
from .factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.mark.user
@pytest.mark.model
class TestUserModel:
    @pytest.mark.usefixtures("django_db_reset_sequences")
    def test_init(self):
        obj = UserFactory.create()
        assert obj.pk is not None, "Should create a new User instance"
        assert str(obj) == obj.username, "Stringification should return username"