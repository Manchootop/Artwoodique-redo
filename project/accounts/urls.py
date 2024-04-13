from django.urls import path

from project.accounts.views import RegisterView, LoginView, logout_user, ProfileView, ProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/<int:pk>', ProfileView.as_view(), name='details profile'),
    # path('profile/wishlist/', ProfileView.as_view(), name='profile wishlist'),
    path('profile/edit/<int:pk>/', ProfileUpdateView.as_view(), name='update_profile')
]
