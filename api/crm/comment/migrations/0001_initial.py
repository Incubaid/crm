# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 03:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task', '0001_initial'),
        ('contact', '0001_initial'),
        ('sprint', '0001_initial'),
        ('deal', '0001_initial'),
        ('organization', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uid', models.CharField(db_index=True, max_length=4, primary_key=True, serialize=False, unique=True)),
                ('seq', models.IntegerField(unique=True)),
                ('content', markdownx.models.MarkdownxField(max_length=10000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='contact.Contact', verbose_name='contact')),
                ('deal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='deal.Deal', verbose_name='deal')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='organization.Organization', verbose_name='organization')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_owned_by', to='contact.Contact', verbose_name='owner')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='project.Project', verbose_name='project')),
                ('sprint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='sprint.Sprint', verbose_name='sprint')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='task.Task', verbose_name='task')),
            ],
        ),
    ]
