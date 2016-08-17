#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  This file contains a class definition to add the Clients model
  into the django administration.
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"

# Imports
from django.contrib import admin
from .models import Clients

# Class ClientsAdmin
class ClientsAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name',
                       'lastname',
                       'identifier',
                       'physicalCode',
                       'mobileNumber',
                       'email',
                       'birthDate',
		       'insearch'
                       )
        }),
        ('Optional fields', {
            'classes': ('collapse',),
            'fields': (
                       'address',
                       'city',
                       'phoneNumber',
                       'postalCode',
                       'alergies',
                       'diseases',
                       'bloodType',
                       ),
        }),
    )

admin.site.register(Clients, ClientsAdmin)
