# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-13 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='private_access',
            field=models.BooleanField(default=True),
        ),
    ]