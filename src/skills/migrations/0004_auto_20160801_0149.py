# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0003_auto_20160730_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.TextField(default='', verbose_name='description'),
        ),
    ]
