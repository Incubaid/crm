# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import datetime

from django.core.exceptions import ValidationError
from markdownx.models import MarkdownxField


from django.db import models

from contact.models import Contact
from crm.utils import generate_uid, model_to_dict, validate_epoch, generate_seq
from sprint.models import Sprint
from task.models import Task
from deal.models import Deal
from organization.models import Organization
from project.models import Project


class MessageContact(models.Model):
    message = models.ForeignKey(
        'Message',
        verbose_name='message',
        related_name='contacts'
    )

    contact = models.ForeignKey(
        Contact,
        verbose_name='contact',
        related_name='messages'
    )

class Message(models.Model):
    CHANNELS = (
        ('TELEGRAM', 'TELEGRAM'),
        ('EMAIL', 'EMAIL'),
        ('SMS', 'SMS'),
        ('INTERCOM', 'INTERCOM'),
    )

    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    seq = models.IntegerField(
        unique=True,
    )

    title = models.CharField(
        max_length=120,
        db_index=True
    )

    content = MarkdownxField(
        max_length=10000,
        blank=True
    )

    tosend_time = models.IntegerField(
        validators=[validate_epoch]
    )

    send_time = models.IntegerField(
        null=True,
        blank=True,
        validators=[validate_epoch]
    )

    organization = models.ForeignKey(
        Organization,
        related_name='messages',
        null=True,
        blank=True,
        db_index=True
    )

    deal = models.ForeignKey(
        Deal,
        null=True,
        blank=True,
        db_index=True
    )

    project = models.ForeignKey(
        Project,
        related_name='messages',
        null=True,
        blank=True,
        db_index=True
    )

    task = models.ForeignKey(
        Task,
        related_name='messages',
        null=True,
        blank=True,
        db_index=True
    )

    sprint = models.ForeignKey(
        Sprint,
        related_name='messages',
        null=True,
        blank=True,
        db_index=True
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNELS,
        db_index=True

    )

    require_confirmation = models.BooleanField(
        default=False
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
            raise ValidationError({choosed[0]: 'Choose only an organization, comment, project, deal or task'})
        elif len(choosed) == 0:
            raise ValidationError({'organization': 'Choose a organization, comment, project, deal or task'})

        if self.tosend_time < int(time.time()):
            raise ValidationError({'tosend_time': 'Must be future epoch'})

        if self.send_time and self.send_time < self.tosend_time:
            raise ValidationError({'send_time': 'Must be >=  tosend_time'})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            self.seq = generate_seq(self.__class__)
            super(Message, self).save(*args, **kwargs)
        else:
            Message.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.title
