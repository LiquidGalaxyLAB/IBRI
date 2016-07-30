from django.db import models

# Create your models here.
#from __future__ import unicode_literals

from django.db import models

from encrypted_fields import *
# Create your models here.
from clients.models import Clients
from drones.models import Drone


class Route(models.Model):
    mission = models.ForeignKey('Mission')
    baseLat = EncryptedCharField(verbose_name="Base Latitude", max_length=30)
    baseLng = EncryptedCharField(verbose_name="Base Longitude", max_length=30)
    drone = models.ForeignKey(Drone)
    tmpLat = EncryptedCharField(verbose_name="Tmp Latitude", max_length=30)
    tmpLng = EncryptedCharField(verbose_name="Tmp Longitude", max_length=30)
    initialWp = EncryptedIntegerField(verbose_name="Initial Waypoints in Route")
    
    def __unicode__(self):
        return "Route #{} (Mission #{})".format(self.pk, self.mission.pk)

class WayPoint(models.Model):
    route = models.ForeignKey(Route)
    ref = models.IntegerField(verbose_name="Ref.Point")
    lat = EncryptedCharField(verbose_name="Latitude", max_length=30)
    lng = EncryptedCharField(verbose_name="Longitude", max_length=30)
    visited = EncryptedBooleanField(verbose_name="Visited", default=False)
    signalFound = EncryptedIntegerField(verbose_name="Beacon signal detected", null=True)
    photo = EncryptedTextField(verbose_name="Base64 Photo", null=True)

    def __unicode__(self):
        return 'M{}D{}R{} - P#{} - {}, {} '.format(self.route.mission.pk, self.route.drone.pk, self.route.pk, self.ref, self.lat, self.lng)

class Mission(models.Model):
    inSearch = models.ManyToManyField(Clients, verbose_name='In Search')

    def __unicode__(self):
        return 'Mission #{}'.format(self.pk)