from django.conf.urls import url
from .views import searchMap, createRoute, getTracking, setTracking

urlpatterns = [
    url(r'^map/', searchMap),
    url(r'^createRoute/', createRoute, name='createRoute'),
    url(r'^getTracking/', getTracking, name='getTracking'),
    url(r'^setTracking/', setTracking, name='setTracking'),
]