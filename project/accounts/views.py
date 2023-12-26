from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from project.accounts.forms import UserRegisterForm

UserModel = get_user_model()


class LoginView(auth_views.LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')


class RegisterView(views.CreateView, SuccessMessageMixin):
    form_class = UserRegisterForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('login')
    success_message = "Your profile was created successfully"

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()
