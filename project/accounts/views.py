from django.contrib.auth import get_user_model, login
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
        return reverse_lazy('index')


# class RegisterView(views.CreateView, SuccessMessageMixin):
#     form_class = UserRegisterForm
#     template_name = 'account/register.html'
#     success_url = reverse_lazy('login')
#     success_message = "Your profile was created successfully"
#
#     def get_success_url(self):
#         if self.success_url:
#             return self.success_url
#         return super().get_success_url()


class RegisterView(views.CreateView):
    template_name = 'account/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy("index")

    # def form_valid(self, form):
    #     # Check if the form is valid before proceeding
    #     if form.is_valid():
    #         # Save the form to create the user
    #         self.object = form.save()
    #
    #         # Log in the user after registration
    #         login(self.request, self.object)
    #
    #     # Redirect to the success URL
    #     return super().form_valid(form)