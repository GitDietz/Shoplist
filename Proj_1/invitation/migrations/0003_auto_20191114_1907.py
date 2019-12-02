# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-11-14 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_shopgroup_disabled'),
        ('invitation', '0002_auto_20191112_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitationuser',
            name='inviter',
        ),
        migrations.AddField(
            model_name='invitationkey',
            name='invite_to_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.ShopGroup'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='InvitationUser',
        ),
    ]