#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  This file contains a class definition to add the Drone model
  into the Django administration.
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
from django.contrib import admin
from drones.models import Drone

# Register admin Drone into the django admin
admin.site.register(Drone)
