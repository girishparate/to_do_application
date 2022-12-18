from django.test import Client
import unittest
from datetime import datetime
# Create your tests here.

from django.http import response


class TaskGet(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def main_dashboard_get(self):
        response = self.client.get("http://127.0.0.1:8000")
        print(response.status_code)

    def to_do_crud_operation_get(self):
        response = self.client.get("http://127.0.0.1:8000/task-details/new-data-object")
        print(response.status_code)

    def label_crud_operation_get(self):
        response = self.client.get("http://127.0.0.1:8000/label-task/label-example")
        print(response.status_code)


class TaskPost(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')
        self.datetime = datetime.now()

    def main_dashboard_post(self):
        data = {'title': 'new data object', 'note': 'Sample Note', 'reminds_on': self.datetime, 'archive': 'On'}
        response = self.client.post("http://127.0.0.1:8000/", data)
        print(response.status_code)

    def label_crud_operation_post(self):
        data = {'label_title': 'label example'}
        response = self.client.post("http://127.0.0.1:8000/", data)
        print(response.status_code)


class TaskPut(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')
        self.datetime = datetime.now()

    def task_crud_put(self):
        data = {'title': 'new data object edit', 'note': 'Sample Note', 'reminds_on': self.datetime, 'completed': 'On'}
        response = self.client.put("http://127.0.0.1:8000/task-delete-edit/1", data)
        print(response.status_code)

    def label_crud_put(self):
        data = {'label_title': 'label example edit'}
        response = self.client.put("http://127.0.0.1:8000/label-delete-edit/1", data)
        print(response.status_code)


class TaskDelete(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')
        self.datetime = datetime.now()

    def task_crud_delete(self):
        response = self.client.delete("http://127.0.0.1:8000/task-delete-edit/1")
        print(response.status_code)

    def label_crud_delete(self):
        response = self.client.delete("http://127.0.0.1:8000/label-delete-edit/1")
        print(response.status_code)
