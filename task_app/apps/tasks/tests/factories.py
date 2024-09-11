from factory import Faker
from factory.django import DjangoModelFactory

from tasks.models import Task


class TaskFactory(DjangoModelFactory):
    name = Faker('name')
    description = Faker('text')
    is_done = Faker('boolean')

    class Meta:
        model = Task
