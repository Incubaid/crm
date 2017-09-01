# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from django.shortcuts import render
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter

from .models import Project


class ProjectAdmin(admin.ModelAdmin):
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
        'promoter__first_name',
        'promoter__last_name',
        'guardian__first_name',
        'guardian__last_name',
        'parent__name',
        'users__first_name',
        'users__last_name'
    ]

    def view(self, obj):
        return '<a href="/admin/project/project/%s/review/" title="Display">%s</a> <a href="/admin/project/project/%s/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit project"></a>' % (obj.uid, obj.name, obj.uid)

    view.allow_tags = True
    view.short_description = 'Review/Edit'

    review_template = 'project.html'

    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='project_review')
        ]

        return my_urls + urls

    def review(self, request, id):
        entry = Project.objects.get(pk=id)
        root_path = '/admin/project/project'
        contact_root_path = '/admin/contact/contact'
        task_root_path = '/admin/task/task'
        sprint_root_path = '/admin/sprint/sprint'
        organization_root_path = '/admin/organization/organization'
        deal_root_path = '/admin/deal/deal'
        edit_url = '%s/%s' % (root_path, id)
        promoter_url = '%s/%s' % (contact_root_path, entry.promoter.uid)
        guardian_url = '%s/%s' % (contact_root_path, entry.guardian.uid)
        parent_url = '%s/%s' % (root_path, entry.parent.uid) if entry.parent else ''
        return render(request, self.review_template, {
            'title': mark_safe('%s <a href="%s"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>' % (entry.name, edit_url)),
            'project': entry,
            'opts': self.model._meta,
            'root_path': root_path,
            'edit_url': edit_url,
            'promoter_url': promoter_url,
            'guardian_url': guardian_url,
            'parent_url': parent_url,
            'sprint_root_path': sprint_root_path,
            'contact_root_path': contact_root_path,
            'organization_root_path':organization_root_path,
            'deal_root_path':deal_root_path,
            'task_root_path': task_root_path,
            'review_url': '/admin/project/project/%s/review' % id,
            'change': '',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False
        })

admin.site.register(Project, ProjectAdmin)
