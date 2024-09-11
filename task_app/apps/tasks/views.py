from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter

from tasks.filters import TaskFilterBackend, TaskFilterSet
from tasks.models import Task
from tasks.serializers import TaskModelSerializer


class TaskGenericViewSet(viewsets.ModelViewSet):
    serializer_class = TaskModelSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Task.objects.all()
    filter_backends = (TaskFilterBackend, DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filterset_class = TaskFilterSet
