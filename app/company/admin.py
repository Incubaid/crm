# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter

from deal.models import Deal
from .models import Company, CompanyPhone, CompanyEmail
from django.shortcuts import render


class CompanyPhoneInline(admin.TabularInline):
    model = CompanyPhone


class CompanyEmailInline(admin.TabularInline):
    model = CompanyEmail

class CompanyDealInline(admin.TabularInline):
    readonly_fields = ('uid',)
    model = Deal
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('uid',)
    list_display = ('view', 'owner_view', 'owner_backup_view', 'created_at', 'modified_at', 'isuser')
    search_fields = [
        'name',
        'description',
        'owner__first_name',
        'owner__last_name',
        'owner_backup__first_name',
        'owner_backup__last_name',
        'emails__email',
        'phone_numbers__phone'
    ]

    list_filter = (
        ('created_at', DateRangeFilter),
        ('modified_at', DateRangeFilter),
    )

    inlines = (
        CompanyPhoneInline,
        CompanyEmailInline,
        CompanyDealInline
    )

    def view(self, obj):
        return '<a href="/admin/company/company/%s/review/" title="Display"><img src="" />%s</a><a href="/admin/company/company/%s/change/"><img src="/static/admin/img/icon-changelink.svg" alt="Edit comment"></a>' % (obj.uid, obj.name, obj.uid)

    view.allow_tags = True
    view.short_description = 'Review/Edit'

    def owner_view(self, obj):
        if obj.owner:
            return '<a href="/admin/contact/contact/%s/review/" title="Display"><img src="" />%s</a>' % (obj.owner.uid, obj.owner.name)
        return '-'

    owner_view.allow_tags = True
    owner_view.short_description = 'Owner'

    def owner_backup_view(self, obj):
        if obj.owner_backup:
            return '<a href="/admin/contact/contact/%s/review/" title="Display"><img src="" />%s</a>' % (obj.owner_backup.uid, obj.owner_backup.name)
        return '-'

    owner_backup_view.allow_tags = True
    owner_backup_view.short_description = 'Owner backup'

    review_template = 'company.html'

    def get_urls(self):
        urls = super(CompanyAdmin, self).get_urls()

        my_urls = [
            url(r'(?P<id>\w+)/review/$', self.review, name='company_review')
        ]

        return my_urls + urls

    def review(self, request, id):
        entry = Company.objects.get(pk=id)
        root_path = '/admin/company/company'
        contact_root_path = '/admin/contact/contact'
        company_root_path = '/admin/company/company'
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
            'company_root_path':company_root_path,
            'contact_root_path': contact_root_path,
            'organization_root_path': organization_root_path,
            'project_root_path':project_root_path,
            'deal_root_path': deal_root_path,
            'task_root_path': task_root_path,
            'comment_root_path':comment_root_path,
            'review_url': '/admin/project/project/%s/review' % id,
            'edit_url': edit_url,
            'company': entry,
            'opts': self.model._meta,
            'root_path': '/admin/company/company',
            'change':'',
            'is_popup': False,
            'save_as': False,
            'has_delete_permission':False,
            'has_add_permission': False,
            'has_change_permission':False
        })

admin.site.register(Company, CompanyAdmin)
