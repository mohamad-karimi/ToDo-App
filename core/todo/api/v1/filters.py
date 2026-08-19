from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from ...models import Tasks

User = get_user_model()


class TasksFilter(filters.FilterSet):
    """
    Create a custom filter class for filtering tasks
    by user and completion status.
    """

    user = filters.ModelMultipleChoiceFilter(
        field_name="user", queryset=User.objects.all()
    )

    class Meta:
        """
        Set the model and define the fields available for filtering.
        """

        model = Tasks
        fields = ["user", "completed"]
