from rest_framework.fields import CurrentUserDefault


class CurrentUserOrNoneDefault(CurrentUserDefault):
    """
    Prevents AnonymousUser from getting into User fk field
    """

    def __call__(self, serializer_field):
        user = serializer_field.context['request'].user
        return user if user.is_authenticated else None
