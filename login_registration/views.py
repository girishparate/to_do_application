from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.shortcuts import redirect
from django.conf import settings


class Registration(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration.html'

    def get(self, request):
        data = {"title": "Registration"}
        return Response(data=data)

    def post(self, request):

        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        hashed_password = make_password(password)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address already registered.")
        else:
            User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email, password=hashed_password).save()
        return redirect('/')


class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        data = {"title": "Login"}
        return Response(data=data)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        data = {}
        if User.objects.filter(email=email).exists():
            user= User.objects.get(email=email)
            if check_password(password, user.password):
                login(request, user)
                return redirect('/')
        else:
            messages.error(request, 'Email not registered.')
        return redirect('/')


class Logout(APIView):
    def get(self, request):
        logout(request)
        return redirect('/')


"""if password is forgotten the send link on registered email"""


class ForgotPassword(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'forgot_password.html'

    def get(self, request):
        data = {"title": "Forgot Password"}
        return Response(data)

    def post(self, request):
        email = request.POST.get('email')

        # If user exists in DB, send reset password email on registered email
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            recipients = [email]

            current_site = get_current_site(request)
            subject = 'Reset Password'
            message = render_to_string('set-password-email-template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            msg = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, recipients)
            msg.content_subtype = 'html'
            msg.send()
            messages.success(request, 'Please check your email for resetting password.')
            return redirect('/')

        # Else display error
        else:
            messages.error(request, 'Please enter registered email.')

        return redirect('/')


"""the above link sent will be redirecting you here"""


class ResetPassword(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reset_password.html'

    def get(self, request, uidb64, token):
        # If user is accessing reset password view with valid URL, display reset password view
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            data = {"title": "Password Reset", 'user': user}
            return Response(data)

        # Else display error    
        else:
            messages.error(request, 'Activation link is invalid.')
            return redirect('/')

    def post(self, request, email):
        # Get all parameters
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # If both passwords match, reset password
        if password and confirm_password is not None:
            if password == confirm_password:
                try:
                    u = User.objects.get(email=email)
                    u.set_password(password)
                    u.save()
                    return redirect('/')
                except:
                    messages.error(request, 'Email not registered.')

            # Else display error        
            else:
                messages.error(request, 'Passwords do not match.')

        # Else display error
        else:
            messages.error(request, 'Please enter password.')