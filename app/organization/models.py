# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from contact.models import Contact
from crm.utils import generate_uid, model_to_dict
from markdownx.models import MarkdownxField

class Organization(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    name = models.CharField(
        max_length=120,
        db_index=True
    )

    description = MarkdownxField(
        max_length=10000,
        db_index=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    promoter = models.ForeignKey(
        Contact,
        verbose_name='Promoter',
        related_name='organizations_promoted_by',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    guardian = models.ForeignKey(
        Contact,
        verbose_name='Guardian',
        related_name='organizations_guarded_by',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    parent = models.ForeignKey(
        'Organization',
        verbose_name='parent',
        related_name='children',
        null=True,
        blank=True
    )

    users = models.ManyToManyField(
        Contact,
        related_name='organizations'
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            super(Organization, self).save(*args, **kwargs)
        else:
            Organization.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.name
