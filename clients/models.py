# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from encrypted_fields import *

# Create your models here.
from django.contrib.auth.models import User

class Clients(models.Model):

    name = EncryptedCharField(max_length=50, verbose_name="First Name", blank=False)
    lastname = EncryptedCharField(max_length=50, verbose_name="Last Name", blank=False)
    email = EncryptedEmailField(max_length=100, verbose_name="Email address")
    identifier = EncryptedCharField(max_length=9, verbose_name="Identifier", unique=True, blank=False)
    physicalCode = EncryptedCharField(max_length=32, blank=False, verbose_name="Physical Code", unique=True)
    address = EncryptedCharField(max_length=100, blank=True)
    city = EncryptedCharField(max_length=100, blank=True)
    phoneValidator = RegexValidator(regex=r'^\+?\d{9,12}?$', message="Phone number must be entered in the format: '+34612345678' or '612345678'.")
    mobileNumber = EncryptedCharField(validators=[phoneValidator], max_length=20, verbose_name="Mobile Phone Number", blank=False)
    phoneNumber = EncryptedCharField(validators=[phoneValidator], max_length=20, verbose_name="Contact Phone Number", blank=True)
    birthDate = EncryptedDateField(verbose_name="Birth Date", blank=False)
    postalCode = EncryptedCharField(max_length=10, verbose_name="Postal Code", blank=True)
    alergies = EncryptedCharField(max_length=500, verbose_name="Alergies", blank=True)
    diseases = EncryptedCharField(max_length=500, verbose_name="Diseases", blank=True)
    #contacts = models.ManyToManyField("self", blank=True)
    insearch = EncryptedBooleanField(verbose_name="In search", default=False)
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
        return u"{} - {}, {} <{}>".format(self.identifier, self.name, self.lastname, self.email)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
