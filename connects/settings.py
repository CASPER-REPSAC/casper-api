from pathlib import Path
from datetime import timedelta
import os, json

# json parse for key
with open('connects/keys.json') as key_file:
    json_file = json.load(key_file)
    json_secret_key = json_file["settings-secret-key"]

    default_ENGINE = json_file["default-database-ENGINE"]
    default_NAME = json_file["default-database-NAME"]
    default_USER = json_file["default-database-USER"]
    default_PW = json_file["default-database-PASSWORD"]
    default_HOST = json_file["default-database-HOST"]
    default_PORT = json_file["default-database-PORT"]
    STATE = json_file["STATE"]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')
MEDIA_URL = './files/'

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     STATIC_DIR,
# ]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
SECRET_KEY = json_secret_key

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Feature : Managing
    'managing',

    # Feature : Create Activity
    'activity',

    # Feature: SocialLogin
    'accounts',

    # django-rest framework
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',

    #CORS
    'corsheaders',
    
    # api doc module
    # 'drf-yasg',

    # dj-rest-auth
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',

    # 'rest_auth',
    # 'rest_auth.registration'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
}

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

##CORS
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS = True #전체 주소 허용 
# 특정 주소 허용 
# CORS_ORIGIN_WHITELIST = (
#     'www.mysite.com',
#     'www.anothersite.com'
# )

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

ROOT_URLCONF = 'connects.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['activity/static'],
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
        'ENGINE': default_ENGINE,
        'NAME': default_NAME,
        'USER': default_USER,
        'PASSWORD': default_PW,
        'HOST': default_HOST,
        'PORT': default_PORT,
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

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# USE_X_FORWARDED_HOST = True

AUTH_USER_MODEL = 'accounts.User'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None # username 필드 사용 x
ACCOUNT_EMAIL_REQUIRED = True            # email 필드 사용 o
ACCOUNT_USERNAME_REQUIRED = False        # username 필드 사용 x
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# JWT Configuration
REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

