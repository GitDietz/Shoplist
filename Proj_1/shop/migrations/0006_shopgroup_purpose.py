# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2020-02-20 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200218_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopgroup',
            name='purpose',
            field=models.CharField(default='Because I can', max_length=200),
            preserve_default=False,
        ),
    ]
