# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-09 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0023_auto_20180509_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imges',
            name='imges',
            field=models.ImageField(default='noimg.jpg', upload_to='imges/%Y/%m/%d/'),
        ),
    ]