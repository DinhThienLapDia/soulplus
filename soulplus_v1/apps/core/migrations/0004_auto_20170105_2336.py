# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-05 16:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': 'Like', 'verbose_name_plural': 'Likes'},
        ),
        migrations.AlterModelOptions(
            name='privategroup',
            options={'verbose_name': 'PrivateGroup', 'verbose_name_plural': 'PrivateGroup'},
        ),
    ]
