from django.contrib import messages
from django.contrib.auth import views as auth_views, logout, get_user_model, login, user_logged_in
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views, View

from project.accounts.forms import ProfileUpdateForm, UserRegisterForm1
from project.accounts.models import ArtwoodiqueUserProfile
from project.engagements.models import WishList

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
    form_class = UserRegisterForm1
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


class ProfileView(LoginRequiredMixin, views.DetailView):
    template_name = 'account/user_profile.html'
    queryset = UserModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_instance = get_object_or_404(ArtwoodiqueUserProfile, user=self.request.user)
        context['user'] = self.request.user
        context['profile'] = profile_instance
        context['profile_form'] = ProfileUpdateForm(instance=profile_instance)
        return context


# class ProfileUpdateView(views.UpdateView):
#     queryset = ArtwoodiqueUserProfile.objects.all()
#     form_class = ProfileUpdateForm
#     template_name = 'store.html'
#
#     def get_success_url(self):
#         messages.success(self.request, 'Your profile was updated successfully')
#         return reverse("details profile", kwargs={
#             "pk": self.object.pk,
#         })
#

class ProfileUpdateView(views.View):
    @staticmethod
    def post(request, pk):
        form = ProfileUpdateForm(request.POST)


        if form.is_valid():
            # Get or create the profile instance for the current user
            profile_instance, created = ArtwoodiqueUserProfile.objects.get_or_create(user=request.user)
            # Check if the profile instance already exists
            if not created:
                # Compare fields of the existing instance with the form data
                if profile_instance.name == form.cleaned_data['name'] \
                        and profile_instance.date_of_birth == form.cleaned_data['date_of_birth'] \
                        and profile_instance.gender == form.cleaned_data['gender']:
                    # No changes were made to the profile
                    messages.info(request, 'No changes were made to your profile')
                    return redirect(reverse('details profile', kwargs={'pk': profile_instance.pk}))
            # Update the profile instance with the form data
            form = ProfileUpdateForm(request.POST, instance=profile_instance)
            # Save the profile instance
            profile_instance = form.save(commit=False)
            profile_instance.user = request.user  # Set the user
            profile_instance.save()
            messages.success(request, 'Your profile was updated successfully')
            return redirect(reverse('details profile', kwargs={'pk': profile_instance.pk}))
        # If form is invalid or other errors occur
        messages.error(request, f'{form.errors.as_text()}')
        return redirect(reverse('details profile', kwargs={'pk': pk}))

