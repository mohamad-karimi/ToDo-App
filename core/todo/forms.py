from django import forms
from .models import Tasks


class TodoForm(forms.ModelForm):
    """
    A form for creating and updating Todo objects.

    This form is connected to the Todo model and only includes
    the title field, allowing users to enter or edit todo titles.
    """

    class Meta:
        model = Tasks
        fields = ("title",)
