#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  This file contains the routing from main package
"""

# Django imports
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

# Own imports
import config.urls
from search.views import searchMap, createRoute, getTracking, setTracking, setDroneTracking, getDroneMissionData
import clients.urls
from clients.views import ulogin
from utils.weatherApi import getWeather

urlpatterns = [
	url(r'login/', ulogin, name="login"),
    url(r'^u/', include(admin.site.urls)),
    url(r'^admin/', include(config.urls)),
    url(r'^p/', include(clients.urls)),
    url(r'^createRoute/$', createRoute, name='createRoute'),
    url(r'^getTracking/$', getTracking, name='getTracking'),
    url(r'^setTracking/$', setTracking, name='setTracking'),
    url(r'^setDroneTracking/$', setDroneTracking, name='setDroneTracking'),
    url(r'^getDroneMissionData/(?P<droneId>[0-9]+)/$', getDroneMissionData, name='getDroneMissionData'),
    url(r'^getWeather/(?P<lat>[+-]?[0-9]+\.[0-9]+)/(?P<lng>[+-]?[0-9]+\.[0-9]+)/', csrf_exempt(getWeather), name='getWeather'),
    url(r'^', searchMap, name='searchMap'),
]
