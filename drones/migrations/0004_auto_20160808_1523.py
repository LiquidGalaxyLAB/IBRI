# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-08 15:23
from __future__ import unicode_literals

from django.db import migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('drones', '0003_remove_drone_dronespeed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='droneRef',
            field=encrypted_fields.fields.EncryptedCharField(max_length=20, unique=True, verbose_name='Ref'),
        ),
    ]
