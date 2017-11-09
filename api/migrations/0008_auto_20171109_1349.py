# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20171109_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tableTitle', models.TextField(max_length=50, unique=True)),
                ('tableDescription', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.DeleteModel(
            name='Board',
        ),
        migrations.AlterField(
            model_name='card',
            name='boardID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Table'),
        ),
        migrations.DeleteModel(
            name='Set',
        ),
    ]