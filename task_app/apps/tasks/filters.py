from django_filters import OrderingFilter
from rest_framework.filters import BaseFilterBackend
from django_filters.rest_framework import FilterSet

from tasks.models import Task


class TaskFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.get_available_for_user(request.user)


class TaskFilterSet(FilterSet):
    order_by = OrderingFilter(fields=(('created_at', 'created_at'),))

    field_labels = {
        'created_at': 'Created at',
    }

    class Meta:
        model = Task
        fields = ['is_done', 'order_by']
