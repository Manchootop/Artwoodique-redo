import os
from pathlib import Path
import cloudinary
import dj_database_url
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
# Read SECRET_KEY from the file
# if DEBUG:
#     with open('secret_key.txt') as f:
#         SECRET_KEY = f.read().strip()
SECRET_KEY = 'django-insecure-=(!&olqxy6ni=d_7_)#x6#9rhs9(oad+@h%f1(+utjc-8k99a+'
DEBUG = True
IS_PRODUCTION = False
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'project.main',
    'project.accounts',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    'django_countries',
    'crispy_bootstrap5',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if IS_PRODUCTION:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    cloudinary.config(
        cloud_name="dzkpnriaw",
        api_key="549581289117547",
        api_secret="Jwd3ECNeENCxeCcEE3LZyx1DY14"
    )
if IS_PRODUCTION:
    MIDDLEWARE += 'whitenoise.middleware.WhiteNoiseMiddleware',
ROOT_URLCONF = 'project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.main.context_processors.newsletter_signup_form',
            ],
        },
    },
]
WSGI_APPLICATION = 'project.wsgi.application'
if IS_PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "artwoodique-original_db",
            "USER": "mkaurgxzzuaiyu",
            "PASSWORD": "dc5916eff18122b15dfbdc152cc06ddf9215f66fd4e616c9b77de0f3d3ba9b27",
            "HOST": "ec2-34-251-233-253.eu-west-1.compute.amazonaws.com",
            "PORT": "5432",
        }
    }
    DATABASES = {
        "default": dj_database_url.config(default=os.environ.get("DATABASE_URL1"))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "artwoodique-original_db",
            "USER": "postgres",
            "PASSWORD": "Thatshurt",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }

if not IS_PRODUCTION:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if IS_PRODUCTION:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'mediafiles'
MEDIA_URL = '/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FROM_EMAIL = "mariqn5000@gmail.com"

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use the appropriate port for your email provider
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mariqn5000@gmail.com'
EMAIL_HOST_PASSWORD = 'mgtn nqyr leaz sidv '
ACCOUNT_EMAIL_VERIFICATION = 'none'
STRIPE_SECRET_KEY = "sk_test_Thatshurt74408K"
STRIPE_PUBLIC_KEY = "bla bla bla "
# settings.py
LOGIN_REDIRECT_URL = '/'
# AUTH_USER_MODEL = 'accounts.ArtwoodiqueUser'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
if IS_PRODUCTION:
    # SECURE_SSL_REDIRECT = True

    SECURE_SSL_CERTIFICATE = '../ssl_cert/certificate.crt'
    SECURE_SSL_KEY = '../ssl_cert/private.key'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

# Set email as the required field for registration
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': 'your-google-client-id',
#             'secret': 'your-google-client-secret',
#             'key': '',
#         }
#     },
#     'facebook': {
#         'APP': {
#             'client_id': 'your-facebook-app-id',
#             'secret': 'your-facebook-app-secret',
#             'key': '',
#             'scope': ['email', 'public_profile'],
#             'fields': [
#                 'id',
#                 'email',
#                 'name',
#                 'first_name',
#                 'last_name',
#                 'verified',
#                 'locale',
#                 'timezone',
#                 'link',
#                 'gender',
#                 'updated_time',
#             ],
#             'version': 'v12.0',
#         }
#     },
#     # Add other providers if needed
# }
CONTACT_EMAIL = 'artwoodique@gmail.com'
