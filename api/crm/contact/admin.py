# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from reversion.admin import VersionAdmin
from rangefilter.filter import DateRangeFilter

from .models import Contact, MessageChannel, ContactPhone,  ContactEmail

class ContactPhoneInline(admin.TabularInline):
    model = ContactPhone


class ContactEmailInline(admin.TabularInline):
    model = ContactEmail

class ContactMessageChannel(admin.TabularInline):
    model = MessageChannel

class ContactAdmin(VersionAdmin):
    readonly_fields = ('uid', 'seq')

    list_display = ('pk', 'message_channels', 'first_name', 'last_name', 'telegram', 'created_at', 'modified_at')
    list_filter = (
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
    )

    inlines = (
        ContactPhoneInline,
        ContactEmailInline,
        ContactMessageChannel

    )

    search_fields = [
                    'first_name',
                    'last_name',
                    'description',
                    'owner__first_name',
                    'owner__last_name',
                    'owner_backup__first_name',
                    'owner_backup__last_name',
                    'telegram',
                    'emails__email',
                    'phone_numbers__phone'
    ]

admin.site.register(Contact, ContactAdmin)
