# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-23 01:06
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0013_file_imges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='내용'),
        ),
    ]
