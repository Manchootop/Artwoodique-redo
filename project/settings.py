import os
from datetime import timedelta
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

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'project.main',
    'project.accounts',
    'project.orders',
    'project.payments',
    'project.shared',
    'project.engagements',
    'project.designer',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'paypal.standard.ipn',
    'rest_framework',
    'django_countries',
    'crispy_bootstrap5',
    'paypal',
]


INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'allauth.account.middleware.AccountMiddleware',
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
                'project.engagements.context_processors.newsletter_signup_form',
                'project.accounts.context_processors.profile_context_processor',
            ],
            'builtins': [
                'project.shared.templatetags.cart_item_count',
                'project.shared.templatetags.extract_decimal_part_from_a_number',
                'project.shared.templatetags.get_name_first_letters',
                'project.shared.templatetags.wishlist_item_count',
            ],
        },
    },
]
WSGI_APPLICATION = 'project.wsgi.application'
if IS_PRODUCTION:
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.postgresql",
    #         "NAME": "artwoodique-original_db",
    #         "USER": "mkaurgxzzuaiyu",
    #         "PASSWORD": "dc5916eff18122b15dfbdc152cc06ddf9215f66fd4e616c9b77de0f3d3ba9b27",
    #         "HOST": "ec2-34-251-233-253.eu-west-1.compute.amazonaws.com",
    #         "PORT": "5432",
    #     }
    # }
    DATABASES = {
        "default": dj_database_url.config(default=os.environ.get("DATABASE_URL1"))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "artwoodique_exam",
            "USER": "postgres",
            "PASSWORD": "Thatshurt",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',
    #     }
    # }

if not IS_PRODUCTION and not DEBUG:
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
DEFAULT_FROM_EMAIL = "artwoodique@gmail.com"

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use the appropriate port for your email provider
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'artwoodique@gmail.com'
EMAIL_HOST_PASSWORD = 'mgtn nqyr leaz sidv'
ACCOUNT_EMAIL_VERIFICATION = 'none'
STRIPE_SECRET_KEY = "sk_test_Thatshurt74408K"
STRIPE_PUBLIC_KEY = "bla bla bla "
# settings.py
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.ArtwoodiqueUser'
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

CONTACT_EMAIL = 'artwoodique@gmail.com'

PAYPAL_RECEIVER_EMAIL = 'bussiness_acc@gmail.com'
PAYPAL_TEST = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}



