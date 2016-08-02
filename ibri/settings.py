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
    #'debug_toolbar'
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

# Weather Map API
WMAPAPI = ''

# Secret Preshared Key
SKEY = '' # Example: LHnhUqmgS1KWh4

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['static/', 'static/dist/', 'static/pages/',
        os.path.join(BASE_DIR, 'static/'),
        os.path.join(BASE_DIR, 'static/dist/'),
        os.path.join(BASE_DIR, 'static/pages/'),
        ],
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

IBRI_URL = ''

try:
    from local_settings import *
except ImportError:
    pass

ibriLogo = """
       @8CoocoCO@              8CoocooO8        
    @C::oO@@@@Ooc:o8        O::cO8@@@8Cc:c8     
   C:o8@8oc::ccO@@C:o     O:c8@8oc:::cC@@C:c@   
  o:O@O:cO@   8o:C@8cc@  C:C@O:cO@   8o:o@@c:8  
 O:o@C:C        8cc@O:C 8:o O:o        @cc@8:o  
 C:O@cc@         o:8@:o O:O o:8         C:O@cc@ 
 O:C@o:O                                o:88cc  
 @cc8@o:C     @:::::::o 8:::::::O     8c:8@o:O  
   o:O@8o::co @:::::::o 8c::::::O Occ:cO@8c:O   
    Oc:o8     @:::::::o 8:::::::O     @Oc:o     
       Occ::c @:::c::cC 8c:c::c:O O:::cC8       
                                                
      8o:::co @:::::::C 8:::::::C Occ::cC@      
    C:cO@@@8@ @c::::::o 8:::::::C @8@@@@o:c8    
  8cc8@Oc:coC @:::::::o 8:::::::C 8oo::o@@o:C   
 @cc@@cc8     @cccccccC @cccccccO     @o:O@C:C  
 O:C@oc8                                o:8@cc@ 
 C:O@cc@         oc8@:o 8:O o:8         C:O@cc@ 
 8:o@O:o        O:o@O:C @cc 8:c@       8:o@O:o  
  C:o@8c:o8@@8C::C@O:o   O:o@@o:oO@@@O:cC@8cc   
   8c:O@@OoccoO@@8c:C     8c:C@@8CocoC@@8c:C    
     8c:coCOOOCc:cO         8o::oCOOOCc:cC@     
         8OCCO8@                8OCCC8@         

   IBRI :: INTERACTION BEACON RESCUE INTERFACE
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

if WMAPAPI == '':
    print colored('ERROR: WMAPAPI is empty', 'red')
    print "Please, set WMAPAPI constant in ibri/settings.py or local_settings.py. The constant should contain a OpenWeatherMap " \
          "API. More info at http://openweathermap.org/api"
    sys.exit()
else:
    print colored('✔ WMapAPI: '+WMAPAPI, 'green')

if SKEY == '':
    print colored('ERROR: SKEY (Secret Preshared Key) is empty', 'red')
    print "Please, set SKEY constant in ibri/settings.py or local_settings.py (14 chars length)"
    sys.exit()
else:
    print colored('✔ SKEY: '+(len(SKEY) * "*"), 'green')

if IBRI_URL == '':
    print colored('ERROR: IBRI_URL is empty', 'red')
    print "Please, set IBRI_URL constant in ibri/settings.py or local_settings.py to the URL where is placed the web service (without the slash at the end)"
    sys.exit()
else:
    print colored('✔ IBRI_URL: '+IBRI_URL, 'green')