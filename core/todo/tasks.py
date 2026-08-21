from celery import shared_task
from .models import Tasks

@shared_task
def delete_completed_tasks():
    tasks = Tasks.objects.filter(completed=True)
    tasks.delete()