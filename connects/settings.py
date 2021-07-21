"""
Django settings for connects project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

#for key
import json

#JWT Configuration
REST_USE_JWT = True

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' : timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME' : timedelta(days=7),
    'ROTATE_REFRESH_TOKENS' : False,
    'BLACKLIST_AFTER_ROTATION': True,
}

#json parse for key
with open ('connects/keys.json','r') as key_file:
    json_file = json.load(key_file)
    json_secret_key = json_file("settings-secret-key")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = json_secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #django-rest framework
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    #dj-rest-auth
    'dj-rest-auth',
    'dj-rest-auth.registration',
    #djang-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    #restapi for study info : apps.py
    'restapi.apps.RestapiConfig',
    #restapi for google auth : apps.py
    'userapi.apps.UserapiConfig',   
   
    #api doc module
    #'drf-yasg',
]

#SITE_ID = 
AUTH_USER_MODEL = 'userapi.User'

REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES' :(
      'rest_framework.permissions.IsAuthenticated',
  ),
  'DEFAULT_AUTHENTICATION_CLASSES' :(
    'rest_framework.authentication.SessionAuthentication',
    'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
}

USERAPI_USER_MODEL_USERNAME_FIELD = None
USERAPI_USER_EMAIL_REQUIRED = True
USERAPI_USERNAME_REQUIRED = False
USERAPI_AUTHENTICATION_METHOD = 'email'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'connects.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'connects.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apidb',        #db name    / default_set : BASE_DIR / 'db.sqlite3',
        'USER':'apiuser',          #db id
        'PASSWORD' : 'apipw',        #db pw
        'HOST' : 'localhost',   #host ip
        'PORT' : '3306',        #port
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
