from django.contrib import admin

# Register your models here.
from search.models import Route, WayPoint, Mission

admin.site.register(WayPoint)
admin.site.register(Route)

class WayPointAdmin(admin.ModelAdmin):
    ordering = ['pk']

class MissionAdmin(admin.ModelAdmin):
    filter_horizontal = ['inSearch']

admin.site.register(Mission, MissionAdmin)
