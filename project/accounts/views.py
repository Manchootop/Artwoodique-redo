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
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('index')


class RegisterView(views.CreateView):
    template_name = 'accounts/register.html'
    form_class = UserRegisterForm1
    success_url = reverse_lazy("index")



class ProfileView(LoginRequiredMixin, views.DetailView):
    template_name = 'accounts/user_profile.html'
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
            profile_instance, created = ArtwoodiqueUserProfile.objects.get_or_create(user=request.user)

            if not created:

                if profile_instance.username == form.cleaned_data['username'] \
                        and profile_instance.date_of_birth == form.cleaned_data['date_of_birth'] \
                        and profile_instance.gender == form.cleaned_data['gender'] \
                        and profile_instance.first_name == form.cleaned_data['first_name'] \
                        and profile_instance.last_name == form.cleaned_data['last_name']:
                    messages.info(request, 'No changes were made to your profile')
                    return redirect(reverse('details profile', kwargs={'pk': profile_instance.pk}))

            form = ProfileUpdateForm(request.POST, instance=profile_instance)
            profile_instance = form.save(commit=False)
            profile_instance.user = request.user  # Set the user
            profile_instance.save()


            messages.success(request, 'Your profile was updated successfully')
            return redirect(reverse('details profile', kwargs={'pk': profile_instance.pk}))

        messages.error(request, f'{form.errors.as_text()}')
        return redirect(reverse('details profile', kwargs={'pk': pk}))
