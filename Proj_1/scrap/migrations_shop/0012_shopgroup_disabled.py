# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-11-14 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_item_in_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopgroup',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
