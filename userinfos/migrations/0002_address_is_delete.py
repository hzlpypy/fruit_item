# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-14 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_delete',
            field=models.CharField(default='1', max_length=3),
        ),
    ]
