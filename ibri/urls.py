from django.conf.urls import url, include
from django.contrib import admin

import search.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include(search.urls)),
]
