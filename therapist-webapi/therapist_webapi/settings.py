"""
Django settings for therapist_webapi project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from datetime import timedelta
import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7ebacb4d-10a8-40df-9572-8306ab4c0155'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG'] == 'True'

ALLOWED_HOSTS = ['*']

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'corsheaders',
    'app',
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Define allowed internal IPs (e.g., your server IPs)
ALLOWED_API_IPS = ["99.47.169.178", "127.0.0.1", os.environ['NETWORK_SEGMENT']]  # Replace with your actual internal IPs


CORS_ALLOWED_ORIGINS = [
    os.environ['FRONTEND_WEBAPP_URL'],  # Allow React frontend
]

CORS_ALLOW_CREDENTIALS = True  # Allow cookies

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-api-key",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    # "PUT",
    # "PATCH",
    # "DELETE",
    "OPTIONS"
]

ROOT_URLCONF = 'therapist_webapi.urls'



ENCRYPT_KEY='xOTMiZhMBTWTR8tWbNkifWcCAlBAiWnAboomokIB3-g='

# API Secret Key
API_SECRET_KEY=os.environ['API_SECRET_KEY']

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
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

WSGI_APPLICATION = 'therapist_webapi.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME_MAIN'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT':os.environ['DB_PORT'],
    },
    'campuspt_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT':os.environ['DB_PORT'],
    }
}

DATABASE_ROUTERS = ['therapist_webapi.routers.database_routers.CampusPTRouter']  # Adjust the import path as necessary


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
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

# SECURE_SSL_REDIRECT = True

USER_ADMIN = 'root'


REMINDERS_WEBAPI = os.environ['REMINDERS_WEBAPI']
REGISTRY_WEBAPP = "https://therapist.campusphysicaltherapy.com" #os.environ['REGISTRY_WEBAPP']

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # Change to 30 minutes
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Change to 7 days
}