# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-15 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_auto_20170513_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
