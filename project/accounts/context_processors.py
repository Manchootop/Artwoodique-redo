from django.shortcuts import get_object_or_404
from .models import ArtwoodiqueUserProfile

def profile_context_processor(request):
    profile_instance = None
    if request.user.is_authenticated:
        profile_instance = get_object_or_404(ArtwoodiqueUserProfile, user=request.user)
    return {'profile': profile_instance}