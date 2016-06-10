# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-10 17:35
from __future__ import unicode_literals

from django.db import migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='nif',
        ),
        migrations.AddField(
            model_name='clients',
            name='identifier',
            field=encrypted_fields.fields.EncryptedCharField(default=0, max_length=9, unique=True, verbose_name=b'Identifier'),
            preserve_default=False,
        ),
    ]
