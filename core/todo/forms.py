from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    '''
    This class for set the fields of the todo form
    '''
    class Meta:
        model = Todo
        fields = (
            "title",
        )