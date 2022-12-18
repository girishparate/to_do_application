from django.db import models
from django.contrib.auth.models import User
from todo.models import ToDo
# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_do = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
