#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python imports
from __future__ import unicode_literals

"""
This file contains the Drone model that is used to registered the
drones data.
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"

# Django imports
from django.db import models

# Third party imports
from encrypted_fields import *


class Drone(models.Model):
    """
    Class drone represents the connection between a real instance of a drone
    and the representation in the database.

    @ivar droneRef: String that represents the drone
    Example:
        - DRONE_ID
        - DRONE QUADCOPTER
    """

    droneRef = EncryptedCharField(verbose_name="Ref", max_length=20, unique=True)

    def __unicode__(self):
        """
        Unicode represents the way that the object is represented as string
        """
        return "{}".format(self.droneRef)
