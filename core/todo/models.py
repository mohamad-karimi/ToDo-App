from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Tasks(models.Model):
    """
    Represents a user's todo task.

    Each todo item belongs to a specific user and stores information
    about the task title, completion status, and timestamps.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    completed = models.BooleanField(null=True, default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the title of the todo item as its string representation.
        """
        return self.title
