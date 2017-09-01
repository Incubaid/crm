# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render

# Register your models here.
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter

from .models import Deal

class DealAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)
    list_display = ('view', 'name', 'state', 'type', 'amount', 'currency', 'company_view', )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
         ('closed_date', DateRangeFilter),
    )
    search_fields = [
        'name',
        'remarks',
        'contact__first_name',
        'contact__last_name',
        'company__name',
        'type',
        'state',
        'remarks',
        'amount',
        'currency',
        'owner__first_name',
        'owner__last_name',
        'owner_backup__first_name',
        'owner_backup__last_name',
        'links__url',
        'tasks__title',
    ]

    def view(self, obj):
        return '<a href="/admin/deal/deal/%s/review/" title="Display"><img src="" />%s</a><a href="/admin/deal/deal/%s/change/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit deal"></a>' % (obj.uid, obj.name, obj.uid)

    view.allow_tags = True
    view.short_description = 'Review/Edit'

    def company_view(self, obj):
        if obj.owner:
            return '<a href="/admin/company/company/%s/review/" title="Display"><img src="" />%s</a>' % (obj.company.uid, obj.company.name)
        return '-'

    company_view.allow_tags = True
    company_view.short_description = 'Owner'

    review_template = 'deal.html'

    def get_urls(self):
        urls = super(DealAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='deal_review')
        ]

        return my_urls + urls

    def review(self, request, id):
        entry = Deal.objects.get(pk=id)
        root_path = '/admin/link/link'
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
            'deal': entry,
            'opts': self.model._meta,
            'root_path': '/admin/company/company',
            'change':'',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission':False,
            'has_add_permission': False,
            'has_change_permission':False
        })

admin.site.register(Deal, DealAdmin)