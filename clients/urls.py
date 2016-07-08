from views import showUserData
from django.conf.urls import url

urlpatterns = [
   url(r'(?P<uid>[0-9]+)/$', showUserData, name='getclientdataweb'),
]

