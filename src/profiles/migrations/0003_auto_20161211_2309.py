# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-11 23:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20160906_0029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='description',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='title',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='years_experience',
        ),
    ]