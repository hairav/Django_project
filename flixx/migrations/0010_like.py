# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-01 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flixx', '0009_auto_20171001_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flixx.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flixx.user')),
            ],
        ),
    ]
