# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-27 08:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20160615_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='contacts',
        ),
    ]
