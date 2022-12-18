from django.test import Client
import unittest
# Create your tests here.

from django.http import response


class LoginRegistrationGet(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def registration_get(self):
        response = self.client.get("http://127.0.0.1:8000/login-registration/registration")
        print(response.status_code)

    def login_get(self):
        response = self.client.get("http://127.0.0.1:8000/login-registration/login")
        print(response.status_code)

    def logout_get(self):
        response = self.client.get("http://127.0.0.1:8000/login-registration/logout")
        print(response.status_code)

    def forgot_password_get(self):
        response = self.client.get("http://127.0.0.1:8000/login-registration/forgot-password")
        print(response.status_code)


class LoginRegistrationPost(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def registration_post(self):
        data = {'email': 'admin@gmail.com', 'password': 'admin', 'first_name': 'Girish', 'last_name': 'Parate'}
        response = self.client.post("http://127.0.0.1:8000/login-registration/registration", data)
        print(response.status_code)

    def login_post(self):
        data = {'email': 'admin@gmail.com', 'password': 'admin'}
        response = self.client.post("http://127.0.0.1:8000/login-registration/login", data)
        print(response.status_code)

    def forgot_password_post(self):
        data = {'email': 'admin@gmail.com'}
        response = self.client.post("http://127.0.0.1:8000/login-registration/forgot-password", data)
        print(response.status_code)

    def reset_password_post(self):
        data = {'password': 'admin_pass_update', 'confirm_password': 'admin_pass_update'}
        response = self.client.post("http://127.0.0.1:8000/login-registration/password-reset/admin@gmail.com", data)
        print(response.status_code)
