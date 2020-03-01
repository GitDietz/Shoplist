# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2020-01-01 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_shopgroup_leaders'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='for_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.ShopGroup'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='in_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShopGroup'),
        ),
    ]