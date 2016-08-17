#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  This file contains the routing to server to the client the HTML
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"


# Django imports
from django.conf.urls import url

# Own imports
from .views import showUserData

urlpatterns = [
   url(r'(?P<uid>[0-9]+)/$', showUserData, name='getclientdataweb'),
]