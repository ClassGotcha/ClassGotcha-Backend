"""
Django settings for classgotcha project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import datetime

import os

# ------ Basic Settings ------

PROJECT_APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(PROJECT_APP_ROOT))

with open(os.path.join(PROJECT_APP_ROOT, 'settings/secret.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = False

ALLOWED_HOSTS = []

SITE_ID = 1

# ------ Application definition ------

ROOT_URLCONF = 'classgotcha.urls'
WSGI_APPLICATION = 'classgotcha.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    # installed
    'rest_framework',
    'rest_framework_docs',
    'rest_framework.authtoken',
    'rest_framework_jwt',
    'storages',
    'channels',
    'corsheaders',
    'widget_tweaks',
    # myapp
    'classgotcha.apps.accounts',
    'classgotcha.apps.posts',
    'classgotcha.apps.classrooms',
    'classgotcha.apps.comments',
    'classgotcha.apps.groups',
    'classgotcha.apps.notes',
    'classgotcha.apps.tasks',
    'classgotcha.apps.chat',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # --- account support ---
    # 'account.middleware.LocaleMiddleware',
    # 'account.middleware.TimezoneMiddleware',
]

# ______ Channel Layers_____
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
        "ROUTING": "classgotcha.routing.channel_routing",
    },
}

# ------ Templates ------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': False,
        },
    },
]

# ------ Database ------
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {

}


# ------ Password validation ------
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# ------ Internationalization -------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ------ Static files (CSS, JavaScript, Images) ------
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/templates/statics/'

# ------ Custom User ------
AUTH_USER_MODEL = 'accounts.Account'

# ------ Rest framework ------
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# ------ Amazon S3 ------
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# Amazon Web Services access key, as a string.
AWS_ACCESS_KEY_ID = 'AKIAIC72HESTHUCZQHLQ'
# Amazon Web Services secret access key, as a string.
AWS_SECRET_ACCESS_KEY = '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'
# Amazon Web Services storage bucket name, as a string.
AWS_STORAGE_BUCKET_NAME = 'classgotcha-us-standard-20161024'
# Allow django-admin.py collectstatic to automatically put your static files in your bucket set
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# ----- Cross Origin Header -----
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'google.com',
    'hostname.example.com',
    'localhost:4000',
    '127.0.0.1:9000'
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
    'cache-control'
)