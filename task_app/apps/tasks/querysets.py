from django.db.models import QuerySet, Q


class TaskQuerySet(QuerySet):
    def get_available_for_user(self, user):
        if user.is_authenticated:
            return self.filter(Q(created_by__isnull=True) | Q(created_by=user))
        return self.filter(created_by__isnull=True)
