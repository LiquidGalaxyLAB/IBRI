# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-10 17:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import encrypted_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('drones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inSearch', models.ManyToManyField(to='clients.Clients', verbose_name=b'In Search')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseLat', encrypted_fields.fields.EncryptedCharField(max_length=30, verbose_name=b'Base Latitude')),
                ('baseLng', encrypted_fields.fields.EncryptedCharField(max_length=30, verbose_name=b'Base Longitude')),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drones.Drone')),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Mission')),
            ],
        ),
        migrations.CreateModel(
            name='WayPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', encrypted_fields.fields.EncryptedIntegerField(verbose_name=b'Ref.Point')),
                ('lat', encrypted_fields.fields.EncryptedCharField(max_length=30, verbose_name=b'Latitude')),
                ('lng', encrypted_fields.fields.EncryptedCharField(max_length=30, verbose_name=b'Longitude')),
                ('visited', encrypted_fields.fields.EncryptedBooleanField(default=False, verbose_name=b'VisiModeted')),
                ('signalFound', encrypted_fields.fields.EncryptedIntegerField(null=True, verbose_name=b'Beacon signal detected')),
                ('photo', encrypted_fields.fields.EncryptedTextField(null=True, verbose_name=b'Base64 Photo')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Route')),
            ],
        ),
    ]
