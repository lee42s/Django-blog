# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-09 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0027_auto_20180509_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imges',
            name='noimge',
        ),
        migrations.AlterField(
            model_name='imges',
            name='imges',
            field=models.ImageField(blank=True, default='static/img/noimg.jpg', upload_to='imges/%Y/%m/%d/'),
        ),
    ]
