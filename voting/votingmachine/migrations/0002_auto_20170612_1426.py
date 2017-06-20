# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-12 14:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votingmachine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votingmachine.Event'),
        ),
        #migrations.AlterField(
        #    model_name='team',
        #    name='leader',
        #    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to=settings.AUTH_USER_MODEL),
        #),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
