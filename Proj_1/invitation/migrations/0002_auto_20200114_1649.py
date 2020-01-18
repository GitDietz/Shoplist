# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2020-01-14 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitationkey',
            name='invite_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invitationkey',
            name='invited_email',
            field=models.EmailField(default='africanmeats@gmail.com', max_length=254),
            preserve_default=False,
        ),
    ]
