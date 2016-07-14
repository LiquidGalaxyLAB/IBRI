
from django.conf.urls import url, include
from django.contrib import admin

#import search.urls
import config.urls
from search.views import searchMap, createRoute, getTracking, setTracking, setDroneTracking, getDroneMissionData
import clients.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/', include(config.urls)),
    url(r'^p/', include(clients.urls)),
    url(r'^createRoute/$', createRoute, name='createRoute'),
    url(r'^getTracking/$', getTracking, name='getTracking'),
    url(r'^setTracking/$', setTracking, name='setTracking'),
    url(r'^setDroneTracking/$', setDroneTracking, name='setDroneTracking'),
    url(r'^getDroneMissionData/(?P<droneId>[0-9]+)/$', getDroneMissionData, name='getDroneMissionData'),
    url(r'^', searchMap, name='searchMap'),
]
