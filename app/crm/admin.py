from functools import update_wrapper

from django.contrib import admin
from django.conf.urls import url
from django.template import RequestContext
from django.shortcuts import render_to_response


class MyEntryAdmin(admin.ModelAdmin):
    review_template = 'display.html'

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = super(MyEntryAdmin, self).get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = [
            url(r'(?P<id>\d+)/review/$', wrap(self.review), name='%s_%s_review' % info),
        ]

        return my_urls + urls

    def review(self, request, id):
        entry = MyEntry.objects.get(pk=id)

        return render_to_response(self.review_template, {
            'title': 'Review entry: %s' % entry.title,
            'entry': entry,
            'opts': self.model._meta,
            'root_path': self.admin_site.root_path,
        }, context_instance=RequestContext(request))

admin.site.register(MyEntry, MyEntryAdmin)