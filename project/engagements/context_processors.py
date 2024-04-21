from project.engagements.forms import NewsletterSignupForm

def newsletter_signup_form(request):
    return {
        'newsletter_signup_form': NewsletterSignupForm()
    }