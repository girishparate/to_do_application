from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    label_title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.label_title


class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    label = models.ManyToManyField(Label)
    title = models.CharField(max_length=500)
    note = models.TextField(null=True)
    reminder = models.BooleanField(default=False)
    reminds_on = models.DateTimeField(null=True)
    image = models.FileField(upload_to='to_do', null=True)
    archive = models.BooleanField(default=False)
    task_id = models.TextField(null=True)
    completed = models.BooleanField(default=False)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title


class Collaborator(models.Model):
    task = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email
