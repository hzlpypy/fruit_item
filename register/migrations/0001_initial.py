# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-09 03:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=32, verbose_name='用户名')),
                ('upwd', models.CharField(max_length=32, verbose_name='密码')),
                ('uemail', models.EmailField(max_length=32, verbose_name='邮箱')),
                ('create_data', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('isDelete', models.CharField(default='1', max_length=32)),
            ],
            options={
                'db_table': 'userinfo',
            },
        ),
    ]
