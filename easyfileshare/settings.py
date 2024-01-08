from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent


ON_APP_ENGINE = os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')

print("ON APP: ", ON_APP_ENGINE)

project_id = 'https://easyfileshare.uc.r.appspot.com'
DEBUG = not ON_APP_ENGINE

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

if DEBUG:
    SECRET_KEY = 'random23454k01*(&*^()(&%^-development-secret-key'
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
else:
    SECRET_KEY = get_secret('DJANGO_SECRET_KEY')
    ALLOWED_HOSTS = [project_id]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
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


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if not DEBUG:
    GS_DB_BUCKET_NAME = get_secret("GS_DB_BUCKET_NAME")
    GS_DATABASE_PATH = get_secret("GS_DATABASE_PATH")

    DATABASES = {
        'default': {
            'ENGINE': 'storages.backends.gcloud.GoogleCloudStorage',
            'NAME': f'{GS_DB_BUCKET_NAME}/{GS_DATABASE_PATH}',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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


if not DEBUG and ON_APP_ENGINE:
    GS_BUCKET_NAME = get_secret("GS_BUCKET_NAME")
    STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_OBJECT_CACHE_CONTROL = {
        'static/*': 'public, max-age=3600',
        'media/*': 'public, max-age=0, no-cache, no-store, must-revalidate',
        f'{GS_DATABASE_PATH}': 'no-store, no-cache, must-revalidate',
    }
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'staticfiles'),
    ]
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
