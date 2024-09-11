from random import randint

from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from factory import Faker, lazy_attribute

TEST_USER_PASSWORD = 'SecretPassword1#'


class UserFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    class Meta:
        model = User
        django_get_or_create = ('username', 'email')

    @lazy_attribute
    def email(self):
        rand_int = str(randint(1, 1000))
        return f'{self.first_name.lower()}_{self.last_name.lower()}_{rand_int}@example.com'

    @lazy_attribute
    def username(self):
        return self.email.split('@')[0]
