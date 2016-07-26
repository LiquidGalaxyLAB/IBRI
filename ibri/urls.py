
from django.conf.urls import url, include
from django.contrib import admin

#import search.urls
import config.urls
from search.views import searchMap, createRoute, getTracking, setTracking, setDroneTracking, getDroneMissionData
import clients.urls
from clients.views import ulogin
from django.contrib.auth.views import logout

urlpatterns = [
	url(r'login/', ulogin, name="login"),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^u/', include(admin.site.urls)),
    url(r'^admin/', include(config.urls)),
    url(r'^p/', include(clients.urls)),
    url(r'^createRoute/$', createRoute, name='createRoute'),
    url(r'^getTracking/$', getTracking, name='getTracking'),
    url(r'^setTracking/$', setTracking, name='setTracking'),
    url(r'^setDroneTracking/$', setDroneTracking, name='setDroneTracking'),
    url(r'^getDroneMissionData/(?P<droneId>[0-9]+)/$', getDroneMissionData, name='getDroneMissionData'),
    url(r'^', searchMap, name='searchMap'),
]
