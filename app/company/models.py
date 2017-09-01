# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from contact.models import Contact
from crm.utils import generate_uid, model_to_dict
from markdownx.models import MarkdownxField

class CompanyPhone(models.Model):
    phone = models.CharField(
        max_length=15,
        db_index=True
    )

    company = models.ForeignKey(
        'Company',
        verbose_name='company',
        related_name='phone_numbers',
        on_delete=models.CASCADE)

class CompanyEmail(models.Model):
    email = models.CharField(
        max_length=40,
        db_index=True,
    )

    company = models.ForeignKey(
        'Company',
        verbose_name='company',
        related_name='emails',
        on_delete=models.CASCADE)

class Company(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    name = models.CharField(
        max_length=50,
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

    owner = models.ForeignKey(
        Contact,
        verbose_name='owner',
        related_name='companies_owned_by',
    )

    owner_backup = models.ForeignKey(
        Contact,
        verbose_name='owner_backup',
        related_name='companies_backedup_by',
        null=True,
        blank=True
    )

    isuser = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            super(Company, self).save(*args, **kwargs)
        else:
            Company.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
