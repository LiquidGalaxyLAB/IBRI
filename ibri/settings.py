# -*- coding: utf-8 -*-

"""
Django settings for IBRI GSoC16 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from termcolor import colored


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qks)%)oulg&!j4v4%t0*)b()naevd+zp4dc^=5u@ti^!8a_=&s'

# SECURITY WARNING: keep the secret keys under control
ENCRYPTED_FIELDS_KEYDIR = 'fieldkeys'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


APPEND_SLASH = True
SECURE_BROWSER_XSS_FILTER = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'search',
    'clients',
    'drones',
    'config',
    'debug_toolbar'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ibri.urls'

WSGI_APPLICATION = 'ibri.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-EN'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True

# KML Directory
KML_DIR = '' # No slash at the end
KML_ICON = '' # URL - If empty, appears a yellow placemark

# Google Shortener API
# https://console.developers.google.com
GAPI = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['static/', 'static/dist/', 'static/pages/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static').replace('\\','/'),)

try:
    from local_settings import *
except ImportError:
    pass

ibriLogo = """
                   ,:.     ::`
                  : . '  ,.```;
                 ;.. : ; ,;` '``
                 ,;   ;;` .   `;
                 ,;           `;
                 '`:`;;;`;; .;.
                  '  ;;;`;;  ,:
                   `.... .. .
                  .':;;'`;; ;;
                 .`,:;;;`;; ; ;
                 ;;  :;;`;;  : ,
                 .;   ::` `   .;
                 :'   :;` :  . :
                 : ';;`. ;`';,:
                  ::.;,   ',.'


      '`  +++++++++++'   .:::::::::::.   +
      @# +@@@@@@@@@@@@@  ';;;;;;;;;;;;;  @+
      @# +@          .@              ;;  @+
      @+ +@++++++++++@@   .::::::::::;;  @+
      @+ +@@@@@@@@@@@@@  .;;;;;;;;;;;;`  @+
      @+ +@          `@  ;;      :;;;    @+
      @+ +@''''''''''@@  ;;        ,;;,  @+
      @+ '@@@@@@@@@@@@'  ';          ;;  @'

============================================================================
============================================================================
"""

print ibriLogo

if KML_DIR == '':
    print colored('ERROR: KML_DIR is empty', 'red')
    print "Please, set KML_DIR constant in ibri/settings.py or local_settings.py. The constant should have a fullpath" \
          " that includes a writable directory to save the KML files inside it"
    sys.exit()
else:
    print colored('✔ KML_DIR: '+KML_DIR, 'green')

if GAPI == '':
    print colored('ERROR: GAPI (Google Api) is empty', 'red')
    print "Please, set GAPI constant in ibri/settings.py or local_settings.py. The constant should contain a Google " \
          "API to use with Google URL Shortener. More info at https://console.developers.google.com"
    sys.exit()
else:
    print colored('✔ GAPI (Google Api): '+GAPI, 'green')