from django.contrib import admin

# Register your models here.
#from search.models import Mission, Waypoints, Route
from search.models import Route, WayPoint, Mission

admin.site.register(WayPoint)
admin.site.register(Route)
#admin.site.register(Mission)

class WayPointAdmin(admin.ModelAdmin):
    ordering = ['pk']

class MissionAdmin(admin.ModelAdmin):
    filter_horizontal = ['inSearch']

admin.site.register(Mission, MissionAdmin)

#admin.site.register(Waypoints)
#admin.site.register(Mission)
#admin.site.register(Route)
