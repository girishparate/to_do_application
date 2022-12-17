from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('notification-list', login_required(NotificationPage.as_view()), name='notification-list'),

    path('read/<pk>', login_required(NotificationRead.as_view()), name='notification-read')
]
