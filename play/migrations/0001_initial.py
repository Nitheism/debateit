# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('reply_channel_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PairUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username_a', models.CharField(max_length=150)),
                ('username_b', models.CharField(max_length=150)),
                ('reply_channel_a', models.CharField(max_length=255)),
                ('reply_channel_b', models.CharField(max_length=255)),
                ('score_a', models.FloatField(blank=True, default=0, null=True)),
                ('score_b', models.FloatField(blank=True, default=0, null=True)),
                ('args_count_a', models.IntegerField(blank=True, default=0, null=True)),
                ('args_count_b', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThemesForDebate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=150)),
            ],
        ),
    ]
