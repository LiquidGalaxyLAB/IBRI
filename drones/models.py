from __future__ import unicode_literals

from django.db import models
from encrypted_fields import *

# Create your models here.

class Drone(models.Model):
    droneRef = EncryptedCharField(verbose_name="Ref", max_length=20)
    preSharedKey = EncryptedCharField(verbose_name="Pre-Shared Key", max_length=100, unique=True)
    droneSpeed = EncryptedIntegerField(verbose_name="Drone Speed")

    def __unicode__(self):
        return "{}".format(self.droneRef)

#class DroneLog(models.Model):
