# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-22 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
