import os
import logging.config
from decouple import config
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# reading config variables
EMAIL_KEY = config('MAIL_API_KEY') # no default or cast used
EMAIL_FROM = config('MAIL_SENDER')


# DEBUG = config('DEBUG', default=False, cast=bool)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('NEW_SK')
PASSWORD_RESET_TIMEOUT = 600

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# For prod set back to False
# ALLOWED_HOSTS = ['getafix.pythonanywhere.com']
# for PROD activate this again
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # third party
    'crispy_forms',
    'markdown_deux',
    'pagedown',
    # local apps
    # 'comments',
    'shop',
    'invitation',
    # 'work_posts'
]

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
]

SILENCED_SYSTEM_CHECKS = [
    'admin.E408','admin.E409','admin.E410',
]

ROOT_URLCONF = 'Proj_1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'Proj_1.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db3.sqlite3'),
    }
}


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

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Brisbane'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL = '/login/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #'/var/www/static/', hardcoded method not used
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")
# os.path.dirname gets the  directory name one level up
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")
# user uploaded docs



# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_INVITATION_DAYS = 7
INVITATIONS_PER_USER = 7
INVITE_MODE = True
REGISTRATIONS = True # allow registrations to take place

# LOGGING CONFIG
LOG_ROOT = os.path.join(BASE_DIR, 'Logs')
# importing logger settings
try:
    from .logger_settings import *
except Exception as e:
    # in case of any error, pass silently.
    pass
