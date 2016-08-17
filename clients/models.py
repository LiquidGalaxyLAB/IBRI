#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the Client model that is used to registered the
clients user data.
"""

# Metadata
__author__ = 'Moises Lodeiro Santiago'
__credits__ = ['Moises Lodeiro-Santiago']
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = 'Moises Lodeiro-Santiago'
__email__ = "moises.lodeiro[at]gmail.com"
__status__ = "Production"

# Python Imports
import uuid

# Django Imports
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Third party imports
from encrypted_fields import *


class Clients(models.Model):
    """
    The Clients models represents a user instance. This data could be useful
    for the emergency squad to know the user important data as for example the
    phone number, diseases, etc. The most of the data is encrypted in the
    database using AES256 CBC algorithm. The key to crypt or decrypt the data
    is stored in the settings SKEY variable.

    @ivar name: First name of the client
    @ivar lastname: Last name of the client
    @ivar email: An email address
    @ivar identifier: An user identifier. For example a passport id
    @ivar physicalCode: The physical web code (url) is automatically set when user
    is registered
    @ivar address: Home address
    @ivar city: City
    @ivar mobileNumber: Mobile (cell) phone number
    @ivar phoneNumber: Home number
    @ivar birthDate: Birth date (yyyy/mm/dd format)
    @ivar postalCode: Postal code
    @ivar alergies: Alergies that an user can have
    @ivar diseases: Diseases that an user can have
    @ivar insearch: Boolean field that responds to the if an user is in search or not
    @ivar bloodType: Blood type
    @see Encrypted Fields (encrypted_fields)
    @requires: Has a SKEY stablished in the database
    """

    name = EncryptedCharField(
        max_length=50, verbose_name="First Name", blank=False)
    lastname = EncryptedCharField(
        max_length=50, verbose_name="Last Name", blank=False)
    email = EncryptedEmailField(max_length=100, verbose_name="Email address")
    identifier = EncryptedCharField(
        max_length=9, verbose_name="Identifier (for example, the passport id)", unique=True, blank=False)
    physicalCode = models.CharField(
        max_length=32, blank=False, verbose_name="Physical Code", unique=False)
    address = EncryptedCharField(max_length=100, blank=True)
    city = EncryptedCharField(max_length=100, blank=True)
    phoneValidator = RegexValidator(
        regex=r'^\+?\d{9,12}?$', message="Phone number must be entered in the format: '+34612345678' or '612345678'.")
    mobileNumber = EncryptedCharField(validators=[phoneValidator], max_length=20, verbose_name="Mobile Phone Number", blank=False)
    phoneNumber = EncryptedCharField(validators=[
                                     phoneValidator], max_length=20, verbose_name="Contact Phone Number", blank=True)
    birthDate = EncryptedDateField(
        verbose_name="Birth Date (mm/dd/yyyy)", blank=True, null=True)
    postalCode = EncryptedCharField(
        max_length=10, verbose_name="Postal Code", blank=True)
    alergies = EncryptedCharField(
        max_length=500, verbose_name="Alergies", blank=True)
    diseases = EncryptedCharField(
        max_length=500, verbose_name="Diseases", blank=True)
    insearch = models.BooleanField(verbose_name="In search", default=False)
    bloodType = EncryptedCharField(max_length=3, blank=True, choices=(
        ('O-', 'O negative'),
        ('O+', 'O positive'),
        ('B-', 'B negative'),
        ('B+', 'B positive'),
        ('A-', 'A negative'),
        ('A+', 'A positive'),
        ('AB-', 'AB negative'),
        ('AB+', 'AB positive'),
    )
    )

    def __unicode__(self):
        """
        __unicode__ represents the way that the object string is showed
        """
        return u"{} - {}, {} <{}>".format(self.identifier, self.name, self.lastname, self.email)

    class Meta:
        """
        Class Meta represents how the data will be displayed in the django
        admin zone.
        """
        verbose_name = "Client"
        verbose_name_plural = "Clients"
