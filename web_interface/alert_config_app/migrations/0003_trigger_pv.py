# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 22:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alert_config_app', '0002_auto_20170613_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='trigger',
            name='pv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='alert_config_app.Pv'),
        ),
    ]
