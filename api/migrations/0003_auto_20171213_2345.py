# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-13 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_board_private_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='private_access',
            field=models.BooleanField(),
        ),
    ]