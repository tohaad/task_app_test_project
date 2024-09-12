from factory import Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from tasks.models import Task


class TaskFactory(DjangoModelFactory):
    name = Faker('name')
    description = Faker('text')
    status = FuzzyChoice(
        Task.STATUS,
        getter=lambda c: c[0],
    )

    class Meta:
        model = Task
