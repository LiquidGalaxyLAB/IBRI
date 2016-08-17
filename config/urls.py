#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  This file contains the routing from config package
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
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import logout

# Own imports
from config.views import *
from search.views import resumeMission


urlpatterns = [
   # Logout
   url(r'logout/', logout, {'next_page': '/'}, name='logout'),
   # Mission
   url(r'mission/resume/(?P<pk>\d+)/$', staff_member_required(resumeMission), name='resumemission'),
   url(r'mission/view/(?P<pk>\d+)/$', staff_member_required(viewMission), name='viewmission'),
   url(r'mission/list/', staff_member_required(missionList), name='missionlist'),
   url(r'mission/delete/(?P<pk>\d+)/$', staff_member_required(MissionDelete.as_view()), name='deletemission'),
   # Clients
   url(r'client/add/$', staff_member_required(CreateClient.as_view()), name='createclient'),
   url(r'client/list/$', staff_member_required(ListClient.as_view()), name='listclients'),
   url(r'client/delete/(?P<pk>\d+)/$', staff_member_required(ClientDelete.as_view()), name='deleteclient'),
   url(r'client/edit/(?P<pk>[0-9]+)/$', staff_member_required(EditClient.as_view()), name='editclient'),
   # Drone
   url(r'drone/add/', staff_member_required(DroneCreate.as_view()), name='createdrone'),
   url(r'drone/list/', staff_member_required(DroneList), name='dronelist'),
   url(r'drone/delete/(?P<pk>\d+)/', staff_member_required(DroneDelete.as_view()), name='deletedrone'),
   url(r'drone/edit/(?P<pk>[0-9]+)/', staff_member_required(EditDrone.as_view()), name='editdrone'),
   # Download
   url(r'download/(?P<m>[0-9]+)/(?P<r>[0-9]+)/', staff_member_required(downloadfile), name='download'),
   # Default call
   url(r'$', config_area, name='configarea')
]
