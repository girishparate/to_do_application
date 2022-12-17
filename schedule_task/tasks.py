from celery import Celery, shared_task, current_task
from .models import Notification, ToDo
from django.contrib.auth.models import User
app = Celery()

@shared_task
def schedule_todo(todo_id, user_id):
    Notification.objects.create(to_do=ToDo.objects.get(id=todo_id), user=User.objects.get(id=user_id)).save()
    return current_task.request