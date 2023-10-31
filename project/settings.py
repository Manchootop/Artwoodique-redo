import os
from pathlib import Path
import cloudinary
import suit

BASE_DIR = Path(__file__).resolve().parent.parent
# Read SECRET_KEY from the file
# if DEBUG:
#     with open('secret_key.txt') as f:
#         SECRET_KEY = f.read().strip()
SECRET_KEY = 'django-insecure-=(!&olqxy6ni=d_7_)#x6#9rhs9(oad+@h%f1(+utjc-8k99a+'
DEBUG = False
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
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    cloudinary.config(
        cloud_name="dzkpnriaw",
        api_key="549581289117547",
        api_secret="Jwd3ECNeENCxeCcEE3LZyx1DY14"
    )
if not DEBUG:
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
            ],
        },
    },
]
WSGI_APPLICATION = 'project.wsgi.application'
if DEBUG:
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
else:
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
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))
    }
if DEBUG:
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
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'mediafiles'
MEDIA_URL = '/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FROM_EMAIL = "mariqn5000@gmail.com"

STRIPE_SECRET_KEY = "sk_test_Thatshurt74408K"

# settings.py
LOGIN_REDIRECT_URL = '/'
# AUTH_USER_MODEL = 'accounts.ArtwoodiqueUser'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

JET_SIDE_MENU = True

