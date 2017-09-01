# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from functools import update_wrapper

# Register your models here.
from django.shortcuts import render
from  django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter

from .models import Contact, ContactPhone, ContactEmail, MessageChannel


class ContactPhoneInline(admin.TabularInline):
    model = ContactPhone


class ContactEmailInline(admin.TabularInline):
    model = ContactEmail

class ContactMessageChannel(admin.TabularInline):
    model = MessageChannel

class ContactAdmin(admin.ModelAdmin):
    readonly_fields = (
        'uid',)

    list_display = ('view', 'message_channels', 'first_name', 'last_name', 'telegram', 'created_at', 'modified_at')
    list_filter = (
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
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

    def view(self, obj):
        return '<a href="/admin/contact/contact/%s/review/" title="Display"><img src="" />%s</a><a href="/admin/contact/contact/%s/change/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit comment"></a>' % (obj.uid, obj.name, obj.uid)

    view.allow_tags = True
    view.short_description = 'Review/Edit'

    inlines  = (
        ContactPhoneInline,
        ContactEmailInline,
        ContactMessageChannel

    )
    review_template = 'contact.html'

    def get_urls(self):
        urls = super(ContactAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='contact_review')
        ]

        return my_urls + urls

    def review(self, request, id):
        entry = Contact.objects.get(pk=id)
        root_path = '/admin/contact/contact'
        link_root_path = '/admin/link/link'
        contact_root_path = '/admin/contact/contact'
        task_root_path = '/admin/task/task'
        sprint_root_path = '/admin/sprint/sprint'
        company_root_path = '/admin/company/company'
        organization_root_path = '/admin/organization/organization'
        deal_root_path = '/admin/deal/deal'
        comment_root_path = '/admin/comment/comment'
        project_root_path = '/admin/project/project'
        edit_url = '%s/%s' % (root_path, id)
        return render(request, self.review_template, {
            'title': mark_safe('%s <a href="%s"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>' % (entry.name, edit_url)),
            'sprint_root_path': sprint_root_path,
            'link_root_path':link_root_path,
            'contact_root_path': contact_root_path,
            'organization_root_path': organization_root_path,
            'project_root_path':project_root_path,
            'deal_root_path': deal_root_path,
            'task_root_path': task_root_path,
            'comment_root_path':comment_root_path,
            'company_root_path':company_root_path,
            'review_url': '/admin/project/project/%s/review' % id,
            'edit_url': edit_url,
            'contact': entry,
            'opts': self.model._meta,
            'root_path': '/admin/contact/contact',
            'change':'',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission':False,
            'has_add_permission': False,
            'has_change_permission':False
        })

admin.site.register(Contact, ContactAdmin)
admin.site.register(MessageChannel)