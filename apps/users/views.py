from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.conf import settings
import logging
from rest_framework.generics import RetrieveAPIView

from .models import User
from .forms import EmailAuthenticationForm, EmailRegistrationForm
from .serializers import UserSerializer
from .permissions import isSelf

logger = logging.getLogger('main')


# Create your views here.
class LoginView(SuccessMessageMixin, FormView):
    template_name = 'users/login.html'
    form_class = EmailAuthenticationForm
    success_url = settings.LOGIN_REDIRECT_URL
    success_message = "Welcome Back!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)
        logger.info(f'user {user} authenticated succesfully')
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """LogoutView"""


class SignUpView(SuccessMessageMixin, FormView):
    template_name = 'users/signup.html'
    form_class = EmailRegistrationForm
    success_url = settings.LOGIN_REDIRECT_URL
    success_message = (
        'Welcome to our chat app! '
        'Feel free to create new rooms and chat with everyone'
    )

    def form_valid(self, form):
        user = form.save()
        logger.info(f'signup of user {user} into the app')
        login(self.request, user)
        logger.info(f'logging user {user} into the app')
        return super().form_valid(form)


# API VIEWS
class UserAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        isSelf,
    ]
