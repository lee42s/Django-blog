# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-11 08:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_user_is_none_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_none_member',
        ),
    ]