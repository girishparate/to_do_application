from django.test import Client
import unittest
# Create your tests here.

from django.http import response


class ScheduleTaskGet(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def notification_page_get(self):
        response = self.client.get("http://127.0.0.1:8000/notification/notification-list")
        print(response.status_code)

    def notification_read_get(self):
        response = self.client.get("http://127.0.0.1:8000/notification/read/1")
        print(response.status_code)
