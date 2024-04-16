from django import template


register = template.Library()


@register.filter
def get_name_first_letters(request):
    if request.user.is_authenticated:
        from project.accounts.models import ArtwoodiqueUserProfile
        user_profile = ArtwoodiqueUserProfile.objects.get(user=request.user)
        # Split the first and last names and extract the first letter of each
        first_letter = user_profile.first_name[0].upper() if user_profile.first_name else ''
        last_letter = user_profile.last_name[0].upper() if user_profile.last_name else ''
        # Concatenate the first letters and return
        return f"{first_letter}{last_letter}" if first_letter and last_letter else 'AN'
    else:
        return 'AN'
