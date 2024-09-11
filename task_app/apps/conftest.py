import pytest
from rest_framework.test import APIClient

from users.tests.factories import UserFactory, TEST_USER_PASSWORD


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    user = UserFactory()
    user.set_password(TEST_USER_PASSWORD)
    user.save()
    return user
