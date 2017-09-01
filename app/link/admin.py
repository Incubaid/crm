# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from django.utils.safestring import mark_safe

from .models import Link, LinkLabel
from django.conf.urls import url
from django.shortcuts import render


class LinkLabelInline(admin.TabularInline):
    model = LinkLabel


# Register your models here.
class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)
    inlines = (
        LinkLabelInline,
    )

    list_display = ('view', 'url', 'created_at', 'modified_at', 'deal_view', 'project_view', 'organization_view', 'comment_view', 'task_view')

    list_filter = (
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
    )

    search_fields = [
        'description',
        'url',
        'contact__first_name',
        'contact__last_name',
        'organization__name',
        'deal__name',
        'project__name',
        'task__title',
        'labels__label'
    ]

    def project_view(self, obj):
        if obj.project:
            return '<a href="/admin/project/project/%s/review/" title="Display"><img src="" />%s</a>' % (obj.project.uid, obj.project.name)
        return '-'

    def deal_view(self, obj):
        if obj.deal:
            return '<a href="/admin/deal/deal/%s/review/" title="Display"><img src="" />%s</a>' % (
            obj.deal.uid, obj.deal.name)
        return '-'

    def organization_view(self, obj):
        if obj.organization:
            return '<a href="/admin/organization/organization/%s/review/" title="Display"><img src="" />%s</a>' % (
            obj.organization.uid, obj.organization.name)
        return '-'

    def comment_view(self, obj):
        if obj.comment:
            return '<a href="/admin/comment/comment/%s/review/" title="Display"><img src="" />%s</a>' % (
            obj.comment.uid, obj.comment.uid)
        return '-'

    def task_view(self, obj):
        if obj.task:
            return '<a href="/admin/task/task/%s/review/" title="Display"><img src="" />%s</a>' % (
            obj.task.uid, obj.task.title)
        return '-'

    def view(self, obj):
        return '<a href="/admin/link/link/%s/review/" title="Display"><img src="" />%s</a><a href="/admin/link/link/%s/change/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit link"></a>' % (obj.uid, obj.uid, obj.uid)

    project_view.allow_tags = True
    project_view.short_description = 'Project'
    organization_view.allow_tags = True
    organization_view.short_description = 'Organization'
    deal_view.allow_tags = True
    deal_view.short_description = 'Deal'
    view.allow_tags = True
    view.short_description = 'Review/Edit'
    task_view.allow_tags = True
    task_view.short_description = 'Task'
    comment_view.allow_tags = True
    comment_view.short_description = 'Comment'


    review_template = 'link.html'

    def get_urls(self):
        urls = super(LinkAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='link_review')
        ]

        return my_urls + urls

    def review(self, request, id):
        entry = Link.objects.get(pk=id)
        root_path = '/admin/link/link'
        contact_root_path = '/admin/contact/contact'
        task_root_path = '/admin/task/task'
        sprint_root_path = '/admin/sprint/sprint'
        organization_root_path = '/admin/organization/organization'
        deal_root_path = '/admin/deal/deal'
        comment_root_path = '/admin/comment/comment'
        project_root_path = '/admin/project/project'
        edit_url = '%s/%s' % (root_path, id)
        return render(request, self.review_template, {
            'title': mark_safe('%s <a href="%s"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>' % (entry.url, edit_url)),
            'sprint_root_path': sprint_root_path,
            'contact_root_path': contact_root_path,
            'organization_root_path': organization_root_path,
            'project_root_path':project_root_path,
            'deal_root_path': deal_root_path,
            'task_root_path': task_root_path,
            'comment_root_path':comment_root_path,
            'review_url': '/admin/project/project/%s/review' % id,
            'edit_url': edit_url,
            'link': entry,
            'opts': self.model._meta,
            'root_path': '/admin/link/link',
            'change': '',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False
        })

admin.site.register(Link, LinkAdmin)
