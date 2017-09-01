# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter

from link.models import Link
from .models import Comment
from django.shortcuts import render
from django.conf.urls import url


class CommentLinkInline(admin.TabularInline):

    model = Link
    readonly_fields = ('uid',)
    extra = 1

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)
    list_display = ('view', 'deal_view', 'project_view', 'organization_view', 'sprint_view', 'task_view', 'created_at', 'modified_at')
    list_filter = (
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
    )

    search_fields = [
        'uid',
        'content',
        'contact__first_name',
        'contact__last_name',
        'owner__first_name',
        'owner__last_name',
        'organization__name',
        'deal__name',
        'project__name',
        'task__title',
        'sprint__name'
    ]

    inlines = (
        CommentLinkInline,
    )

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

    def sprint_view(self, obj):
        if obj.sprint:
            return '<a href="/admin/sprint/sprint/%s/review/" title="Display"><img src="" />%s</a>' % (
            obj.sprint.uid, obj.sprint.uid)
        return '-'

    def task_view(self, obj):
        if obj.task:
            return '<a href="/admin/task/task/%s/review/" title="Display"><img src="" />%s</a>' % (
            obj.task.uid, obj.task.title)
        return '-'

    def view(self, obj):
        return '<a href="/admin/comment/comment/%s/review/" title="Display"><img src="" />%s</a><a href="/admin/comment/comment/%s/change/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit comment"></a>' % (obj.uid, obj.uid, obj.uid)

    view.allow_tags = True
    view.short_description = 'Review/Edit'

    project_view.allow_tags = True
    project_view.short_description = 'Project'
    deal_view.allow_tags = True
    deal_view.short_description = 'Deal Entry'
    organization_view.allow_tags = True
    organization_view.short_description = 'organization'
    sprint_view.allow_tags = True
    sprint_view.short_description = 'Sprint'
    task_view.allow_tags = True
    task_view.short_description = 'Task'

    review_template = 'comment.html'

    def get_urls(self):
        urls = super(CommentAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='deal_review')
        ]
        return my_urls + urls

    def review(self, request, id):
        entry = Comment.objects.get(pk=id)
        root_path = '/admin/comment/comment'
        contact_root_path = '/admin/contact/contact'
        link_root_path = '/admin/link/link'
        task_root_path = '/admin/task/task'
        sprint_root_path = '/admin/sprint/sprint'
        organization_root_path = '/admin/organization/organization'
        deal_root_path = '/admin/deal/deal'
        comment_root_path = '/admin/comment/comment'
        project_root_path = '/admin/project/project'
        edit_url = '%s/%s' % (root_path, id)
        return render(request, self.review_template, {
            'title': mark_safe('%s <a href="%s"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>' % (entry.uid, edit_url)),
            'comment': entry,
            'link_root_path':link_root_path,
            'sprint_root_path': sprint_root_path,
            'contact_root_path': contact_root_path,
            'organization_root_path': organization_root_path,
            'project_root_path': project_root_path,
            'deal_root_path': deal_root_path,
            'task_root_path': task_root_path,
            'comment_root_path': comment_root_path,
            'review_url': '/admin/project/project/%s/review' % id,
            'edit_url': edit_url,
            'opts': self.model._meta,
            'root_path': root_path,
            'change': '',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False
        })

admin.site.register(Comment, CommentAdmin)