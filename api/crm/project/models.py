# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from contact.models import Contact
from crm.utils import generate_uid, model_to_dict, generate_seq
from markdownx.models import MarkdownxField


class Project(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    seq = models.IntegerField(
        unique=True,
    )

    name = models.CharField(
        max_length=120,
        db_index=True
    )

    description = MarkdownxField(
        max_length=10000,
        blank=True,
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


    promoter = models.ForeignKey(
        Contact,
        verbose_name='Promoter',
        related_name='projects_promoted_by',
        db_index=True

    )

    guardian = models.ForeignKey(
        Contact,
        verbose_name='Guardian',
        related_name='projects_guarded_by',
        db_index=True
    )

    parent = models.ForeignKey(
        'Project',
        verbose_name='parent',
        related_name='children',
        null=True,
        blank=True,
        db_index=True
    )

    users = models.ManyToManyField(
        Contact,
        related_name='projects',
        db_index=True
    )

    @property
    def percent_completed(self):
        done = 0.0
        counter = 0.0
        for task in self.tasks.all():
            done += task.percent_completed
            counter += 1
        if counter:
            return done / counter
        return 0.0

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            self.seq = generate_seq(self.__class__)
            super(Project, self).save(*args, **kwargs)
        else:
            Project.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.name
