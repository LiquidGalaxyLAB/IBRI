
from .views import * #CreateClient, ListClient, config_area, ClientDelete, EditClient, missionList
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import logout

from search.views import resumeMission

urlpatterns = [
   url(r'logout/', logout, {'next_page': '/'}, name='logout'),
   
   url(r'mission/resume/(?P<pk>\d+)/$', staff_member_required(resumeMission), name='resumemission'),
   url(r'mission/view/(?P<pk>\d+)/$', staff_member_required(viewMission), name='viewmission'),
   url(r'mission/list/', staff_member_required(missionList), name='missionlist'),
   url(r'mission/delete/(?P<pk>\d+)/$', staff_member_required(MissionDelete.as_view()), name='deletemission'),
   
   url(r'client/add/$', staff_member_required(CreateClient.as_view()), name='createclient'),
   url(r'client/list/$', staff_member_required(ListClient.as_view()), name='listclients'),
   url(r'client/delete/(?P<pk>\d+)/$', staff_member_required(ClientDelete.as_view()), name='deleteclient'),
   url(r'client/edit/(?P<pk>[0-9]+)/$', staff_member_required(EditClient.as_view()), name='editclient'),
   
   url(r'drone/add/', staff_member_required(CreateClient.as_view()), name='createdrone'),
   url(r'drone/list/', staff_member_required(DroneList), name='dronelist'),
   url(r'drone/delete/(?P<pk>\d+)/', staff_member_required(DroneDelete.as_view()), name='deletedrone'),
   url(r'drone/edit/(?P<pk>[0-9]+)/', staff_member_required(EditClient.as_view()), name='editdrone'),
   

   url(r'$', config_area, name='configarea')
]