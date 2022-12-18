from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import MainDashboard, LabelCrudOperation, ToDoCrudOperation

urlpatterns = [
    path('', login_required(MainDashboard.as_view()), name='main-dashboard'),

    path('task-details/<slug>', login_required(ToDoCrudOperation.as_view()), name='task-details'),

    path('task-delete-edit/<pk>', login_required(ToDoCrudOperation.as_view()), name='task-delete-edit'),
    
    path('label-delete-edit/<pk>', login_required(LabelCrudOperation.as_view()), name='label-delete-edit'),
    
    path('label-post', login_required(LabelCrudOperation.as_view()), name='label-post'),

    path('label-task/<slug>', login_required(LabelCrudOperation.as_view()), name='label-task')
]
