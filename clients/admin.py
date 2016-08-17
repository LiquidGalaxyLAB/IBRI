#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  clients/admin.py
  :author Moises Lodeiro Santiago
  :organization IBRI
  :license GPL

  This file contains a class definition to add the Clients model
  into the django administration.
"""

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
