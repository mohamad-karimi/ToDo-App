from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from ...models import Todo

User = get_user_model()

class TasksFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        field_name='user',
        queryset = User.objects.all()
    )
        
    class Meta():
        model = Todo
        fields = [
            "user",
            "completed"
        ]