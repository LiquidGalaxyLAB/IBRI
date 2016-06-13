from django.conf.urls import url, include
from django.contrib import admin

#import search.urls
import config.urls
from search.views import searchMap, createRoute, getTracking, setTracking

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^config/', include(config.urls)),
    url(r'^', searchMap, name='searchMap'),
    url(r'^createRoute/', createRoute, name='createRoute'),
    url(r'^getTracking/', getTracking, name='getTracking'),
    url(r'^setTracking/', setTracking, name='setTracking'),
]
