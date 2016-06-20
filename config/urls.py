from config.views import CreateClient, EditClient, config_area
from django.conf.urls import url

urlpatterns = [
   url(r'client/add/$', CreateClient.as_view(), name='createclient'),
   url(r'client/edit/(?P<pk>[0-9]+)/$', EditClient.as_view(), name='editclient'),
   url(r'$', config_area, name='configarea')
]

