from django.urls import path
from .views import Login, Logout, ForgotPassword, Registration, ResetPassword

urlpatterns = [
    path('login', Login.as_view(), name='login'),

    path('registration', Registration.as_view(), name='registration'),

    path('logout', Logout.as_view(), name='logout'),

]