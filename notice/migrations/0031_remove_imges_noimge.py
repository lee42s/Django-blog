# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-09 08:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0030_post_imges_check'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imges',
            name='noimge',
        ),
    ]
