# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from contact.models import Contact
from crm.utils import generate_uid, model_to_dict
from organization.models import Organization
from project.models import Project

from markdownx.models import MarkdownxField
from django.core.exceptions import ValidationError

class Sprint(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    name = models.CharField(
        max_length=20,
        db_index=True
    )

    description = MarkdownxField(
        max_length=1000,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    start_date = models.DateField()

    deadline = models.DateField()

    owner = models.ForeignKey(
        Contact,
        verbose_name='owner',
        related_name='sprints',
        db_index = True
    )

    project = models.ForeignKey(
        Project,
        related_name='sprints',
        db_index=True,
        blank=True,
        null=True,
    )

    organization = models.ForeignKey(
        Organization,
        related_name='sprints',
        db_index=True,
        blank=True,
        null=True,
    )

    @property
    def percent_completed(self):
        done = 0.0
        counter = 0.0
        for task in self.tasks.all():
            done += task.percent_completed
            counter += 1
        if not counter:
            return done
        return done / counter

    @property
    def hoursopen_person_max(self):
        return 0.0

    @property
    def hoursopen_person_avg(self):
        return 0.0

    @property
    def hours_open(self):
        return 0.0

    def clean_fields(self, *args, **kwargs):
        if not self.project and not self.organization:
            raise ValidationError({'project': 'Choose a project or an organization or both'})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            super(Sprint, self).save(*args, **kwargs)
        else:
            Sprint.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.name
