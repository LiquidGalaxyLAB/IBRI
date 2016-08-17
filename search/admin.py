#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the definition of search models to admin 
implenetation in the administration panel.
@author: Moises Lodeiro-Santiago
"""

# Django imports
from django.contrib import admin

# Own model imports
from search.models import Route, WayPoint, Mission

class WayPointAdmin(admin.ModelAdmin):
    """
    WayPointAdmin extends admin.ModelAdmin to use the WayPoint model
    into the django admin panel.

    @var ordering: Filter order by public key (id)
    @see: admin.ModelAdmin
    """
    ordering = ['id']


class MissionAdmin(admin.ModelAdmin):
    """
    MissionAdmin extends admin.ModelAdmin to use the Mission model
    into the django admin panel.

    @var filter_horizontal: List inSearch as horizontal form
    @see: admin.ModelAdmin
    """
    filter_horizontal = ['inSearch']

# Register the admins
admin.site.register(Mission, MissionAdmin)
admin.site.register(WayPoint, WayPointAdmin)
admin.site.register(Route)
