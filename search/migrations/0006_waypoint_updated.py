# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-09 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_route_initialwp'),
    ]

    operations = [
        migrations.AddField(
            model_name='waypoint',
            name='updated',
            field=models.DateTimeField(auto_now=True, default="2016-04-22 00:00"),
            preserve_default=False,
        ),
    ]
