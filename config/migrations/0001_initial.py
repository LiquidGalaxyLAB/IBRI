# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-13 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=50, unique=True)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
    ]
