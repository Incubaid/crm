# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.db import models
from markdownx.models import MarkdownxField

# Create your models here.
from company.models import Company
from contact.models import Contact
from crm.utils import generate_uid, model_to_dict


class Deal(models.Model):
    TYPES = (
        ('hoster', 'hoster'),
        ('ito', 'ito'),
        ('pto', 'pto'),
        ('prepto', 'prepto'),
    )

    STATES = (
        ('new', 'new'),
        ('interested', 'interested'),
        ('confirmed', 'confirmed'),
        ('waitingclose', 'waitingclose'),
        ('closed', 'closed'),
    )

    CURRENCIES= (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('AED', 'AED'),
        ('GBP', 'GBP'),
    )

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

    contact = models.ForeignKey(
        Contact,
        verbose_name='contact',
        related_name='deals',
        db_index=True
    )

    company = models.ForeignKey(
        Company,
        verbose_name='company',
        related_name='deals',
        db_index=True
    )

    type = models.CharField(
        max_length=10,
        choices=TYPES,
        db_index=True
    )

    state = models.CharField(
        max_length=20,
        choices=STATES,
        db_index=True
    )

    remarks = MarkdownxField(
        max_length=10000,
        blank=True,
        db_index=True
    )

    amount = models.FloatField(
        validators=[MinValueValidator(0)]
    )

    currency = models.CharField(
        max_length=20,
        choices=CURRENCIES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    closed_date = models.DateField(
        null=True,
        blank=True,
        db_index=True
    )

    owner = models.ForeignKey(
        Contact,
        verbose_name='Owner',
        related_name='deals_owned_by')

    owner_backup = models.ForeignKey(
        Contact,
        verbose_name='Backup owner',
        related_name='deals_backedup_by',
        blank=True,
        null=True
    )

    issuer = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            super(Deal, self).save(*args, **kwargs)
        else:
            Deal.objects.filter(pk=self.pk).update(**model_to_dict(self))

    def __str__(self):
        return self.name
