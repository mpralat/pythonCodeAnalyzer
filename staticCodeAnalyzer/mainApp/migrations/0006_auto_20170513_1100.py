# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-13 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_project_cloned_dir_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='pdf_file',
        ),
        migrations.AddField(
            model_name='report',
            name='path_to_report',
            field=models.CharField(default='', max_length=300),
        ),
    ]