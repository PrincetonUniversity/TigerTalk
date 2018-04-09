# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-06 18:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='category',
        ),
        migrations.AddField(
            model_name='club',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='page.Category'),
        ),
        migrations.RemoveField(
            model_name='club',
            name='leaders',
        ),
        migrations.AddField(
            model_name='club',
            name='leaders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='page.Leader'),
        ),
    ]
