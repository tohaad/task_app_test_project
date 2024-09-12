from rest_framework import serializers

from tasks.models import Task
from tasks.serializer_fields import CurrentUserOrNoneDefault


class TaskModelSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=CurrentUserOrNoneDefault())

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status', 'created_by', 'created_at')
