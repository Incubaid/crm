# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render
from rangefilter.filter import DateRangeFilter
from django.utils.safestring import mark_safe

# Register your models here.
from task.models import Task, TaskAssignment, TaskTracking


class TaskAssignmentInline(admin.TabularInline):
    model = TaskAssignment
    exclude = ('uid',)

class TaskTrackingInline(admin.TabularInline):
    model = TaskTracking
    exclude = ('uid',)

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)
    inlines = (
        TaskAssignmentInline,
    )
    list_display = ('view', 'created_at', 'modified_at')
    list_filter = (
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
    )

    search_fields = [
        'title',
        'type',
        'description',
        'urgency',
        'deal__name',
        'project__name',
        'organization__name',
        'sprint__name',
        'owner__first_name',
        'owner__last_name'
    ]

    def view(self, obj):
        return '<a href="/admin/task/task/%s/review/" title="Display"><img src="" />%s</a><a href="/admin/task/task/%s/change/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit task"></a>' % (obj.uid, obj.title, obj.uid)

    view.allow_tags = True
    view.short_description = 'Review/Edit'

    review_template = 'task.html'

    def get_urls(self):
        urls = super(TaskAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='task_review')
        ]

        return my_urls + urls

    def review(self, request, id):

        entry = Task.objects.get(pk=id)
        root_path = '/admin/task/task'
        contact_root_path = '/admin/contact/contact'
        task_root_path = '/admin/task/task'
        sprint_root_path = '/admin/sprint/sprint'
        project_root_path = '/admin/project/project'
        organization_root_path = '/admin/organization/organization'
        deal_root_path = '/admin/deal/deal'
        edit_url = '%s/%s' % (root_path, id)
        link_root_path = '/admin/link/link'
        return render(request, self.review_template, {
            'title': mark_safe('%s <a href="%s"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>' % (
                entry.title, edit_url)),
            'task': entry,
            'link_root_path': link_root_path,
            'sprint_root_path': sprint_root_path,
            'organization_root_path': organization_root_path,
            'contact_root_path':contact_root_path,
            'deal_root_path': deal_root_path,
            'task_root_path': task_root_path,
            'review_url': '/admin/sprint/sprint/%s/review' % id,
            'project_root_path': project_root_path,
            'edit_url': edit_url,
            'opts': self.model._meta,
            'root_path': '/admin/task/task',
            'change': '',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False
        })


class TaskAssignmentAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)
    inlines = (
        TaskTrackingInline,
    )


class TaskTrackingAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskAssignment, TaskAssignmentAdmin)
admin.site.register(TaskTracking, TaskTrackingAdmin)
