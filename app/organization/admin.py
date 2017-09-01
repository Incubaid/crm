# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from django.shortcuts import render
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter

from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)

    list_filter = (
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
    )

    list_display = ('view', 'created_at', 'modified_at', 'view_promoter', 'view_guardian', 'view_parent')
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
        return '<a href="/admin/organization/organization/%s/review/" title="Display"><img src="" />%s</a><a href="/admin/organization/organization/%s/change/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit organization"></a>' % (obj.uid, obj.name, obj.uid)

    view.allow_tags = True
    view.short_description = 'Review/Edit'

    def view_guardian(self, obj):
        if obj.guardian:
            return '<a href="/admin/contact/contact/%s/review/" title="Display"><img src="" />%s</a>' % (
                obj.guardian.uid, obj.guardian.name)
        return '-'

    view_guardian.allow_tags = True
    view_guardian.short_description = 'Guardian'


    def view_parent(self, obj):
        if obj.parent:
            return '<a href="/admin/organization/organization/%s/review/" title="Display"><img src="" />%s</a>' % (
                obj.parent.uid, obj.parent.name)
        return '-'

    view_parent.allow_tags = True
    view_parent.short_description = 'Parent'

    def view_promoter(self, obj):
        if obj.promoter:
            return '<a href="/admin/contact/contact/%s/review/" title="Display"><img src="" />%s</a>' % (
                obj.promoter.uid, obj.promoter.name)
        return '-'

    view_promoter.allow_tags = True
    view_promoter.short_description = 'Promoter'


    review_template = 'organization.html'

    def get_urls(self):
        urls = super(OrganizationAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='organization_review')
        ]

        return my_urls + urls

    def review(self, request, id):
        entry = Organization.objects.get(pk=id)
        root_path = '/admin/organization/organization'
        contact_root_path = '/admin/contact/contact'
        task_root_path = '/admin/task/task'
        sprint_root_path = '/admin/sprint/sprint'
        organization_root_path = '/admin/organization/organization'
        deal_root_path = '/admin/deal/deal'
        comment_root_path = '/admin/comment/comment'
        project_root_path = '/admin/project/project'
        edit_url = '%s/%s' % (root_path, id)

        return render(request, self.review_template, {
            'title': mark_safe('%s <a href="%s"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>' % (entry.name, edit_url)),
            'sprint_root_path': sprint_root_path,
            'contact_root_path': contact_root_path,
            'organization_root_path': organization_root_path,
            'project_root_path':project_root_path,
            'deal_root_path': deal_root_path,
            'task_root_path': task_root_path,
            'comment_root_path':comment_root_path,
            'review_url': '/admin/project/project/%s/review' % id,
            'edit_url': edit_url,
            'organization': entry,
            'opts': self.model._meta,
            'root_path': '/admin/organization/organization',
            'change': '',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False
        })


admin.site.register(Organization, OrganizationAdmin)
