# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 03:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contact', '0001_initial'),
        ('organization', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('uid', models.CharField(db_index=True, max_length=4, primary_key=True, serialize=False, unique=True)),
                ('seq', models.IntegerField(unique=True)),
                ('name', models.CharField(db_index=True, max_length=20)),
                ('description', markdownx.models.MarkdownxField(db_index=True, max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('deadline', models.DateField()),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='organization.Organization')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='contact.Contact', verbose_name='owner')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='project.Project')),
            ],
        ),
    ]
