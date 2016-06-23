
from config.views import CreateClient, ListClient, config_area, ClientDelete, EditClient
from django.conf.urls import url

urlpatterns = [
   url(r'client/add/$', CreateClient.as_view(), name='createclient'),
   url(r'client/list/$', ListClient.as_view(), name='listclients'),
   url(r'client/delete/(?P<pk>\d+)/$', ClientDelete.as_view(), name='deleteclient'),
   #url(r'client/delete/(?P<pk>\d+)/$', ClientDelete.as_view(), name='deleteclient'),
   url(r'client/edit/(?P<pk>[0-9]+)/$', EditClient.as_view(), name='editclient'),
   url(r'$', config_area, name='configarea')
]

