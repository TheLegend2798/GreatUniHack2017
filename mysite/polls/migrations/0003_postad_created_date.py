# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20171112_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='postad',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
