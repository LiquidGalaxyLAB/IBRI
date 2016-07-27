
from config.views import CreateClient, ListClient, config_area, ClientDelete, EditClient, missionList
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from search.views import resumeMission

urlpatterns = [
   url(r'view/(?P<pk>\d+)/$', staff_member_required(resumeMission), name='resumemission'),
   url(r'mission/list/', staff_member_required(missionList), name='missionlist'),
   url(r'client/add/$', staff_member_required(CreateClient.as_view()), name='createclient'),
   url(r'client/list/$', staff_member_required(ListClient.as_view()), name='listclients'),
   url(r'client/delete/(?P<pk>\d+)/$', staff_member_required(ClientDelete.as_view()), name='deleteclient'),
   url(r'client/edit/(?P<pk>[0-9]+)/$', staff_member_required(EditClient.as_view()), name='editclient'),
   url(r'$', config_area, name='configarea')
]

