# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.contrib.auth import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from contact.models import Contact
from crm.utils import generate_uid, model_to_dict, validate_epoch
from deal.models import Deal
from organization.models import Organization
from project.models import Project
from sprint.models import Sprint
from markdownx.models import MarkdownxField


class TaskAssignment(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )
    contact = models.ForeignKey(
        Contact,
        verbose_name='contact',
        related_name='tasks_assigned',
        on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        'Task',
        verbose_name='task',
        related_name='assignments',
        on_delete=models.CASCADE
    )

    @property
    def percent_completed(self):
        done = 0.0
        for stat in self.stats.all():
            done += stat.time_done
        if not done:
            return done
        return done / self.time_todo

    time_todo = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    @property
    def header(self):
        return '%s (%s)' % (self.task.title, self.contact.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            super(TaskAssignment, self).save(*args, **kwargs)
        else:
            TaskAssignment.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.header

class TaskTracking(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    assignment = models.ForeignKey(
        TaskAssignment,
        verbose_name='assignment',
        related_name='stats',
        on_delete=models.CASCADE
    )

    remark = MarkdownxField(
        max_length=10000,
        blank=True,
    )

    time_done = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    epoch = models.IntegerField(
        blank=True,
        validators=[validate_epoch]
    )

    def save(self, *args, **kwargs):
        if not self.epoch:
            self.epoch = int(time.time())

        if not self.pk:
            self.uid = generate_uid(self.__class__)
            super(TaskTracking, self).save(*args, **kwargs)
        else:
            TaskTracking.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.assignment.header

class Task(models.Model):
    TYPES = (
        ('feature', 'feature'),
        ('question', 'question'),
        ('task', 'task'),
        ('story', 'contact'),
        ('contact', 'contact'),
    )

    URGENCY_TYPES = (
        ('critical', 'critical'),
        ('urgent', 'urgent'),
        ('normal', 'normal'),
        ('minor', 'minor'),
    )

    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    title = models.CharField(
        max_length=120,
        db_index=True
    )

    type = models.CharField(
        max_length=15,
        choices=TYPES,
        db_index=True
    )

    description = MarkdownxField(
        max_length=10000,
        blank=True,
        db_index=True
    )

    urgency = models.CharField(
        max_length=15,
        choices=URGENCY_TYPES,
        db_index=True
    )

    deal = models.ForeignKey(
        Deal,
        null=True,
        blank=True,
        verbose_name='deal',
        related_name='tasks',
        db_index=True
    )

    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        verbose_name='project',
        related_name='tasks',
        db_index=True
    )

    organization = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        verbose_name='organization',
        related_name='tasks',
        db_index=True
    )

    sprint = models.ForeignKey(
        Sprint,
        verbose_name='sprint',
        related_name='tasks',
        db_index=True
    )

    owner = models.ForeignKey(
        Contact,
        verbose_name='owner',
        related_name='tasks_owned_by',
    )

    time_todo = models.FloatField(
        default=0.0,
        validators = [MinValueValidator(0)]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def percent_completed(self):
        done = 0.0
        count = 0.0
        for assignment in self.assignments.all():
            done += assignment.percent_completed
            count += 1
        if not count:
            return 0.0
        return done / count

    @property
    def time_done(self):
        done = 0.0
        for assignment in self.assignments.all():
            for stat in assignment.stats.all():
                done += stat.time_done
        return done

    def clean_fields(self, *args, **kwargs):
        choosed = []

        if self.project:
            choosed.append('project')
        if self.deal:
            choosed.append('deal')
        if self.organization:
            choosed.append('organization')

        if len(choosed) > 1:
            raise ValidationError({choosed[0]: 'Choose only an organization, or project'})
        elif len(choosed) == 0:
            raise ValidationError({'deal': 'Choose an organization, or project'})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            super(Task, self).save(*args, **kwargs)
        else:
            Task.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.title
