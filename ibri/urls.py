
from django.conf.urls import url, include
from django.contrib import admin

#import search.urls
import config.urls
from search.views import searchMap, createRoute, getTracking, setTracking
import clients.urls

urlpatterns = [
    url(r'^django_admin/', include(admin.site.urls)),
    url(r'^admin/', include(config.urls)),
    url(r'^p/', include(clients.urls)),
    url(r'^createRoute/$', createRoute, name='createRoute'),
    url(r'^getTracking/$', getTracking, name='getTracking'),
    url(r'^setTracking/$', setTracking, name='setTracking'),
    url(r'^', searchMap, name='searchMap'),
]
