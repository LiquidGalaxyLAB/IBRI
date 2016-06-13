from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Config(models.Model):

    field = models.CharField(max_length=50, unique=True, db_index=True, primary_key=True)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return self.field
