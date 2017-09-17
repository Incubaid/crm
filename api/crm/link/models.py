# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

from contact.models import Contact
from crm.utils import model_to_dict, generate_uid
from sprint.models import Sprint
from task.models import Task
from deal.models import Deal
from organization.models import Organization
from project.models import Project
from comment.models import Comment

from markdownx.models import MarkdownxField


class LinkLabel(models.Model):
    link = models.ForeignKey(
        'Link',
        verbose_name='link',
        related_name='labels',
        on_delete=models.CASCADE
    )

    label = models.CharField(
        max_length=200
    )

class Link(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    seq = models.IntegerField(
        unique=True,
    )

    description = MarkdownxField(
        max_length=10000,
        blank=True,
        db_index=True
    )

    url = models.URLField(
        db_index=True
    )


    contact = models.ForeignKey(
        Contact,
        verbose_name='contact',
        related_name='links',
        db_index=True
    )

    comment = models.ForeignKey(
        Comment,
        null=True,
        related_name='links',
        blank=True
    )

    organization = models.ForeignKey(
        Organization,
        verbose_name='organization',
        related_name='links',
        null=True,
        blank=True,
        db_index=True
    )

    deal = models.ForeignKey(
        Deal,
        verbose_name='deal',
        related_name='links',
        null=True,
        blank=True,
        db_index=True
    )

    project = models.ForeignKey(
        Project,
        verbose_name='project',
        related_name='links',
        null=True,
        blank=True,
        db_index=True
    )

    task = models.ForeignKey(
        Task,
        verbose_name='task',
        related_name='links',
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

    def clean_fields(self, *args, **kwargs):
        choosed = []
        if self.task:
            choosed.append('task')
        if self.comment:
            choosed.append('comment')
        if self.project:
            choosed.append('project')
        if self.deal:
            choosed.append('deal')
        if self.organization:
            choosed.append('organization')

        if len(choosed) > 1:
            raise ValidationError({choosed[0]: 'Choose only an organization, comment, project, deal or task'})
        elif len(choosed) == 0:
            raise ValidationError({'organization': 'Choose a organization, comment, project, deal or task'})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            self.seq = generate_seq(self.__class__)
            super(Link, self).save(*args, **kwargs)
        else:
            Link.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.contact.name

