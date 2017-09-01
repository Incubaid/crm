# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin

# Register your models here.
from .models import MessageContact, Message


class MessageContactInline(admin.TabularInline):
    model = MessageContact


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)
    search_fields = [
        'title',
        'content',
        'organization__name',
        'deal__name',
        'project__name',
        'task__title',
        'sprint__name',
        'contacts__contact__first_name',
        'contacts__contact__last_name',
    ]
    inlines = (MessageContactInline,)

admin.site.register(Message, MessageAdmin)
