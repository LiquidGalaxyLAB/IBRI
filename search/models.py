#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the model to Search package including the Route,
WayPoint and Mission model.
"""
__author__ = 'Moises Lodeiro-Santiago'

# Django imports
from django.db import models
from django.db import models

# Third party imports
from encrypted_fields import *

# Own imports
from clients.models import Clients
from drones.models import Drone


class Route(models.Model):
    """
    Route model class represents the connection between the Mission model and
    the WayPoint. A route is a container that contains the waypoints. A
    mission could have various routes. Mission 1:n Routes 1:n Waypoints

    @ivar mission: Foreign key from the Mission model
    @ivar baseLat: Base latitude. Is the latitude where the base is placed
    @ivar baseLng: Base longitude. Is the longitude where the base is placed
    @ivar drone: Foreign key from the Drone model
    @ivar tmpLat: A temporary latitude. Represents the temporary latitude of
    the drone
    @ivar tmpLng: A temporary longitude. Represents the temporary longitude of
    the drone
    @ivar initialWp: How much initial waypoints has on mission start
    @see Encrypted Fields (encrypted_fields)
    @see Mission
    @see Drone
    """

    mission = models.ForeignKey('Mission')
    baseLat = EncryptedCharField(verbose_name="Base Latitude", max_length=30)
    baseLng = EncryptedCharField(verbose_name="Base Longitude", max_length=30)
    drone = models.ForeignKey(Drone)
    tmpLat = EncryptedCharField(verbose_name="Tmp Latitude", max_length=30)
    tmpLng = EncryptedCharField(verbose_name="Tmp Longitude", max_length=30)
    initialWp = EncryptedIntegerField(
        verbose_name="Initial Waypoints in Route")

    def __unicode__(self):
        """
        __unicode__ represents the way that the object string is showed
        """
        return "Route #{} (Mission #{})".format(self.pk, self.mission.pk)


class WayPoint(models.Model):
    """
    A WayPoint is a GPS position that the drone should visit in order to
    complete the mission. A waypoints is connected to a Route in this way
    Route 1:n Waypoint.

    @ivar route: A route is a foreign key that let us to know the route
    where is placed this waypoint
    @ivar ref: A reference integer to identify the waypoint in the route
    @ivar lat: GPS Latitude
    @ivar lng: GPS Longitude
    @ivar visited: Boolean field to check if that waypoint has been visited
    @ivar signalFound: The user ID if the drone locates the beacon signal
    @ivar photo: Base64 encoded photo that the drone takes
    @ivar updated: Timestamp that indicates to us when the waypoint has been
    visited
    @see Encrypted Fields (encrypted_fields)
    @see Mission
    @see Route
    @see Drone
    """

    route = models.ForeignKey(Route)
    ref = models.IntegerField(verbose_name="Ref.Point")
    lat = EncryptedCharField(verbose_name="Latitude", max_length=30)
    lng = EncryptedCharField(verbose_name="Longitude", max_length=30)
    visited = EncryptedBooleanField(verbose_name="Visited", default=False)
    signalFound = EncryptedIntegerField(
        verbose_name="Beacon signal detected", null=True)
    photo = EncryptedTextField(verbose_name="Base64 Photo", null=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """
        __unicode__ represents the way that the object string is showed
        """
        hasPhoto = False
        if self.photo != None:
            hasPhoto = True
        return 'M{}D{}R{} - P#{} - {}, {} [{}] '.format(self.route.mission.pk, self.route.drone.pk, self.route.pk, self.ref, self.lat, self.lng, hasPhoto)


class Mission(models.Model):
    """
    A Mission contains the users insearch and is linked to Route model as
    foreign key.

    @ivar inSearch: ManyToManyFields reference to Clients model
    @see Encrypted Fields (encrypted_fields)
    @see Mission
    @see Route
    @see Drone
    @See Clients model
    """
    inSearch = models.ManyToManyField(Clients, verbose_name='In Search')

    def __unicode__(self):
        """
        __unicode__ represents the way that the object string is showed
        """
        return 'Mission #{}'.format(self.pk)
