# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-15 11:24
from __future__ import unicode_literals

from django.db import migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waypoint',
            name='visited',
            field=encrypted_fields.fields.EncryptedBooleanField(default=False, verbose_name=b'Visited'),
        ),
    ]
