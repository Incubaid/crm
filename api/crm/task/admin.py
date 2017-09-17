# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from task.models import Task, TaskAssignment, TaskTracking

admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(TaskTracking)
