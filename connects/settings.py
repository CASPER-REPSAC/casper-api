from pathlib import Path
from datetime import timedelta
import os, json, sys


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
    default_authid = json_file["social_auth_google_client_id"]
    default_authsecret = json_file["social_auth_google_secret"]
    default_state = json_file["state"]
    default_base_url = json_file["base_url"]
    default_siteid = json_file["siteid"]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = 'connects.urls'
BASE_URL = default_base_url
ROOT_DIR = os.path.dirname(BASE_DIR)
STATE = default_state
APPEND_SLASH = True

# For Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')
MEDIA_URL = './'
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024


# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!
SECRET_PATH = os.path.join(ROOT_DIR, '.footprint_secret')
SECRET_BASE_FILE = os.path.join(BASE_DIR, 'connects/keys.json')
SECRET_KEY = json_secret_key
DEBUG = False
ALLOWED_HOSTS = ['*']
SOCIAL_AUTH_GOOGLE_CLIENT_ID = default_authid
SOCIAL_AUTH_GOOGLE_SECRET = default_authsecret
SITE_ID = 3 #default_siteid



# Google configuration
#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = default_authid
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = default_authsecret
#SOCIAL_AUTH_USER_FIELDS=['email','first_name','username','password']
## Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
#SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
#    'https://www.googleapis.com/auth/userinfo.email',
#    'https://www.googleapis.com/auth/userinfo.profile',
#]




# Application definition
INSTALLED_APPS = [
    #CORS
    'corsheaders', 

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Feature : Social Auth
    'accounts',
    # Feature : Managing
    'managing',
    # Feature : Create Activity
    'activity',
    # api doc module
    #'drf_yasg',

    #SSL
    #'sslserver',

    # django rest framework
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
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
]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/connects2.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

'''
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
            'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins','file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
'''


# JWT
REST_USE_JWT = True
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


# REST Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        #'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        #'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        #'drf_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'connects.middleware.CORSMiddleware' ,
]


# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True #전체 주소 허용
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
    'application/json',
    'text/plain',
    '/'
)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]
# 특정 주소 허용 
#CORS_ORIGIN_WHITELIST = [
#     'https://www.connects.casper.or.kr',
#     'http://localhost:8080',
#     'http://127.0.0.1:8080',
#     'http://localhost',
#]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['activity/static'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                #'social_django.context_processors.backends',
                #'social_django.context_processors.login_redirect',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
#TEMPLATE_CONTEXT_PROCESSORS = (
#    'social_django.context_processors.backends',
#    'social_django.context_processors.login_redirect',
#)
WSGI_APPLICATION = 'connects.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
AUTH_USER_MODEL = 'accounts.User'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
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


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# USE_X_FORWARDED_HOST = True
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
STATIC_ROOT = os.path.join(ROOT_DIR, './casper-api/static_root/')


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
