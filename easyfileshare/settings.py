from pathlib import Path
import os
from pathlib import Path

DEBUG = True
PRODUCTION = True

from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', 'random23454k01*(&*^()(&%^-development-secret-key')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', '*').split(',')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'easyfileshare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "template")],
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

WSGI_APPLICATION = 'easyfileshare.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', BASE_DIR / "db.sqlite3"),
        'USER': config('DB_USER', ''),
        'PASSWORD': config('DB_PASSWORD', ''),
        'HOST': config('DB_HOST', ''),
        'PORT': config('DB_PORT', ''),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

if PRODUCTION:
    import google.auth, json
    from google.oauth2 import service_account

    GS_BUCKET_NAME = "easyfileshare"
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.path.join(BASE_DIR, "blackstackhub.json"))

    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
        'prefix': 'admin/*',
    }
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

