# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 21:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boardTitle', models.TextField(max_length=50, unique=True)),
                ('boardDescription', models.TextField(blank=True, max_length=500)),
                ('public_access', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('archiveStatus', models.BooleanField(default=False)),
                ('title', models.TextField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('color', models.CharField(default='#fff9ac', max_length=10)),
                ('uniqueNumber', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tableTitle', models.TextField(max_length=50, unique=True)),
                ('tableDescription', models.TextField(blank=True, max_length=500)),
                ('boardID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Board')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='tableID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Table'),
        ),
    ]
