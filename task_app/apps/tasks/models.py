from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField
from tasks.querysets import TaskQuerySet


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    is_done = models.BooleanField(default=False, verbose_name=_('Is done'))
    created_at = AutoCreatedField(verbose_name=_('Created at'))
    created_by = models.ForeignKey(User, verbose_name=_('Created by'), on_delete=models.SET_NULL, null=True)

    objects = TaskQuerySet.as_manager()

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} Task'
