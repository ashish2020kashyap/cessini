

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&4xhadwvpg8$_x83n9wnzbik$d0o_#e#j8g#-p4cx%kaf4wgwg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['cessini-mails.herokuapp.com',
                        '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'anees.apps.AneesConfig',
    'rest_framework',
    'storages',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
]


SITE_ID = 2


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pritha.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'pritha.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wcdbgfmr',
        'USER': 'wcdbgfmr',
        'PASSWORD': 'HgAn9hftqIqMXQHYTi5sjapXLbrf1n7F',
        'HOST': 'lallah.db.elephantsql.com',
        'PORT': '5432',
    }
}


AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

)





# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

'''
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []
'''
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER='ashish160kumar@gmail.com'
EMAIL_HOST_PASSWORD='luciferkashyap@1'


#MESSAGE_TAGS = {
 #   messages.ERROR:'danger'
#}




USING_S3 = True

if USING_S3:
    # AWS SETTINGS
    AWS_ACCESS_KEY_ID = 'AKIATKNI4ILQ67KU4562'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'cessini'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_USE_SSL =False

    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    # AWS S3 static settings
    STATIC_FOLDER = 'static'
    STATIC_ROOT = 'media'
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATIC_FOLDER)
    STATICFILES_STORAGE = 'pritha.default_storages.StaticStorage'

    # AWS S3 public media settings
    MEDIA_FOLDER = 'media'
    MEDIA_ROOT = 'media/'
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIA_FOLDER)
    DEFAULT_FILE_STORAGE = 'pritha.default_storages.MediaStorage'
else:
    # IF WE ARE WORKING LOCALLY WITHOUT AWS
    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)




# ANY EXTRA STATIC FOLDERS THAT DJANGO SHOULD BE AWARE OF
STATICFILES_DIRS = []




