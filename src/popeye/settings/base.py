"""
Django settings for popeye project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$sb!)hoze=h_nl4fdn1x7-xxl_7ho)su&$z4c=+ywr@*&jr9qo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1',
    '127.0.0.1:8000',
    '127.0.0.1:8080',
    'localhost:8080'

)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

START_APPS = [
    'account',
    'channels',
    'corsheaders'
]

INSTALLED_APPS += START_APPS

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

POPEYE_ENCODE_ALGO = os.environ.get('POPEYE_ENCODE_ALGO', 'HS256')

JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': POPEYE_ENCODE_ALGO,
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_PAYLOAD_HANDLER': 'popeye.utils.jwt.jwt_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'popeye.utils.jwt.jwt_response_payload_handler',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'popeye.urls'

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

WSGI_APPLICATION = 'popeye.wsgi.application'
ASGI_APPLICATION = 'popeye.routing.application'

AUTH_USER_MODEL = 'account.User'

RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER', 'popeye')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS', 'pass1234')
RABBITMQ_DEFAULT_VHOST = os.environ.get('RABBITMQ_DEFAULT_VHOST', '')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'popeye-rabbitmq')
BROKER_URL = (f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}'
              f'@{RABBITMQ_HOST}:5672/{RABBITMQ_DEFAULT_VHOST}')

REDIS_HOST = os.environ.get('REDIS_HOST', 'popeye-redis')
REDIS_CACHE_LOCATION = f'redis://{REDIS_HOST}:6379'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('POSTGRES_SERVICE', 'popeye-db'),
        'NAME': os.environ.get('POSTGRES_DB', 'popeye'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'pass1234'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'USER': os.environ.get('POSTGRES_USER', 'popeye')
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'DB': 1,
        }
    },
}


# Channel layer definitions
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, 6379)],
            "capacity": os.environ.get('channel_layer_capacity', 10000)
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TIMEZONE = TIME_ZONE
CELERYD_TASK_SOFT_TIME_LIMIT = os.environ.get('CELERYD_TASK_SOFT_TIME_LIMIT',
                                              270)  # set to 4 min and 30 sec
CELERYD_TASK_TIME_LIMIT = os.environ.get('CELERYD_TASK_TIME_LIMIT',
                                         300)  # set to 5 min

STATIC_ROOT = 'static'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
MEDIA_URL = '/upload/'
