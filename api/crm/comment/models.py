# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

from contact.models import Contact
from crm.utils import model_to_dict, generate_uid, generate_seq
from sprint.models import Sprint
from task.models import Task
from deal.models import Deal
from organization.models import Organization
from project.models import Project

from markdownx.models import MarkdownxField


class Comment(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    seq = models.IntegerField(
        unique=True,
    )

    content = MarkdownxField(
        max_length=10000
    )

    contact = models.ForeignKey(
        Contact,
        verbose_name='contact',
        related_name='comments'
    )

    organization = models.ForeignKey(
        Organization,
        verbose_name='organization',
        related_name='comments',
        null=True,
        blank=True,
        db_index=True
    )

    deal = models.ForeignKey(
        Deal,
        verbose_name='deal',
        related_name='comments',
        null=True,
        blank=True,
        db_index=True
    )

    project = models.ForeignKey(
        Project,
        verbose_name='project',
        related_name='comments',
        null=True,
        blank=True,
        db_index=True
    )

    task = models.ForeignKey(
        Task,
        verbose_name='task',
        related_name='comments',
        null=True,
        blank=True,
        db_index=True
    )

    sprint = models.ForeignKey(
        Sprint,
        verbose_name='sprint',
        related_name='comments',
        null=True,
        blank=True,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    owner = models.ForeignKey(
        Contact,
        verbose_name='owner',
        related_name='comments_owned_by',
    )

    def clean_fields(self, *args, **kwargs):
        choosed = []
        if self.task:
            choosed.append('task')
        if self.sprint:
            choosed.append('sprint')
        if self.project:
            choosed.append('project')
        if self.deal:
            choosed.append('deal')
        if self.organization:
            choosed.append('organization')

        if len(choosed) > 1:
            raise ValidationError({choosed[0]: 'Choose only a task, sprint, project, deal or organization'})
        elif len(choosed) == 0:
            raise ValidationError({'organization': 'Choose a task, sprint, project, deal or organization'})

    def save(self, *args, **kwargs):

        if not self.pk:
            self.uid = generate_uid(self.__class__)
            self.seq = generate_seq(self.__class__)
            super(Comment, self).save(*args, **kwargs)
        else:
            Comment.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.contact.name


