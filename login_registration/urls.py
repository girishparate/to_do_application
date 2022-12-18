from django.urls import path
from .views import Login, Logout, ForgotPassword, Registration, ResetPassword

urlpatterns = [
    path('login', Login.as_view(), name='login'),

    path('registration', Registration.as_view(), name='registration'),

    path('logout', Logout.as_view(), name='logout'),

    path('forgot-password', ForgotPassword.as_view(), name='forgot-password'),

    path('activate/<uid64>/<token>/', ResetPassword.as_view(), name='activate'),

    path('password-reset/<email>', ResetPassword.as_view(), name='password-reset')

]