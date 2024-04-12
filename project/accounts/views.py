from django.contrib import messages
from django.contrib.auth import views as auth_views, logout, get_user_model, login, user_logged_in
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from project.accounts.forms import UserRegisterForm

UserModel = get_user_model()


class LoginView(auth_views.LoginView, SuccessMessageMixin):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        messages.success(self.request, 'You have been logged in successfully')
        success_url = self.get_success_url()
        # Emit user_logged_in signal
        user_logged_in.send(sender=self.request.user.__class__, request=self.request, user=self.request.user)
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('index')


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
