# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from crm.utils import generate_uid, model_to_dict
from markdownx.models import MarkdownxField
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError


class ContactPhone(models.Model):
    phone = models.CharField(
        max_length=15,
        db_index=True
    )

    contact = models.ForeignKey(
        'Contact',
        verbose_name='contact',
        related_name='phone_numbers',
        on_delete=models.CASCADE
    )


class ContactEmail(models.Model):
    email = models.CharField(
        max_length=40,
        db_index=True,
    )

    contact = models.ForeignKey(
        'Contact',
        verbose_name='contact',
        related_name='emails',
        on_delete=models.CASCADE
    )


class MessageChannel(models.Model):
    CHANNELS = {
        'E': 'Email',
        'S': 'SMS',
        'T': 'Telephone',
        'B': 'Bot',
        'I': 'Intercome'
    }

    contact = models.ForeignKey(
        'Contact',
        related_name='communication_channels',
        on_delete=models.CASCADE
    )

    channel = models.CharField(
        max_length=10,
        choices=CHANNELS.items()
    )

    priority = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(len(CHANNELS))
        ]
    )

    class Meta:
        unique_together = (
            ("channel", "priority", "contact"),
        )

    def __str__(self):
        return '%s%s' % (self.channel, self.priority)


class Contact(models.Model):
    uid = models.CharField(
        max_length=4,
        unique=True,
        db_index=True,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=20,
        db_index=True
    )

    last_name = models.CharField(
        max_length=20,
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

    # Must be optional, otherwiae we can't enter 1st contact
    owner = models.ForeignKey(
        'Contact',
        related_name='contacts_owned_by',
        null=True,
        blank=True
    )
    # Must be optional, otherwiae we can't enter 1st contact
    owner_backup = models.ForeignKey(
        'Contact',
        verbose_name='Owner backup',
        related_name='contacts_backedup_by',
        null=True,
        blank=True
    )

    isuser = models.BooleanField(
        default=False,
        verbose_name='Is user?'
    )

    telegram = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        blank=True,
        null=True,
        verbose_name='Telegram bot'
    )

    @property
    def message_channels(self):
        return ','.join(str(m) for m in self.communication_channels.all())

    # Name is (first_name + last_name)
    @property
    def name(self):
        name = '%s %s' % (self.first_name, self.last_name)
        return name.strip()

    # Make unique uid of 4 chars on save
    def save(self, *args, **kwargs):
        if not self.pk:
            self.uid = generate_uid(self.__class__)
            super(Contact, self).save(*args, **kwargs)
        else:
            Contact.objects.filter(pk=self.pk).update(**model_to_dict(self))

    # Check message_channels doesn't contain
    # What string to display when listing an item of this model
    def __str__(self):
        return self.name
