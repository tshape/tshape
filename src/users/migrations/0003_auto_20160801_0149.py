# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160723_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, null=True, verbose_name='last name'),
        ),
    ]
