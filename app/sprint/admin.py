# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from django.shortcuts import render
from rangefilter.filter import DateRangeFilter

from sprint.models import Sprint


class SprintAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)
    list_display = ('view', 'start_date', 'deadline', 'created_at', 'modified_at')
    list_filter = (
        ('start_date', DateRangeFilter),
        ('deadline', DateRangeFilter),
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
    )
    search_fields = [
        'name',
        'description',
        'owner__first_name',
        'owner__last_name',
        'tasks__title',
        'messages__title'
    ]

    def view(self, obj):
        return '<a href="/admin/sprint/sprint/%s/review/" title="Display"><img src="" />%s</a><a href="/admin/sprint/sprint/%s/change/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit sprint"></a>' % (obj.uid, obj.name, obj.uid)

    view.allow_tags = True
    view.short_description = 'Review/Edit'

    review_template = 'sprint.html'

    def get_urls(self):
        urls = super(SprintAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='sprint_review')
        ]

        return my_urls + urls

    def review(self, request, id):
        entry = Sprint.objects.get(pk=id)
        root_path = '/admin/sprint/sprint'
        contact_root_path = '/admin/contact/contact'
        task_root_path = '/admin/task/task'
        sprint_root_path = '/admin/sprint/sprint'
        project_root_path = '/admin/project/project'
        organization_root_path = '/admin/organization/organization'
        deal_root_path = '/admin/deal/deal'
        edit_url = '%s/%s' % (root_path, id)

        return render(request, self.review_template, {
            'title': mark_safe('%s <a href="%s"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>' % (
                entry.name, edit_url)),
            'sprint': entry,
            'sprint_root_path': sprint_root_path,
            'contact_root_path': contact_root_path,
            'organization_root_path': organization_root_path,
            'deal_root_path': deal_root_path,
            'task_root_path': task_root_path,
            'review_url': '/admin/sprint/sprint/%s/review' % id,
            'project_root_path':project_root_path,
            'edit_url': edit_url,
            'opts': self.model._meta,
            'root_path': '/admin/sprint/sprint',
            'change': '',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False
        })

admin.site.register(Sprint, SprintAdmin)
