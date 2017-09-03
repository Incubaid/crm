from itertools import cycle
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm.collections import InstrumentedList
from flask_admin.model import typefmt
from jinja2 import Markup
from datetime import datetime


def format_instrumented_list(view, context, model, name):
    value = getattr(model, name)
    out = ""

    if isinstance(value, InstrumentedList):
        out = "<ul>"
        for x in value:
            if hasattr(x, "admin_view_link"):
                out += "<li><a href='{}'>{}</a></li>".format(
                    getattr(x, "admin_view_link")(), x)
            else:
                out += str(x)
        out += "</ul>"
    return Markup(out)


def format_url(view, context, model, name):
    value = getattr(model, name)
    return Markup("<a href='{url}'>{url}</a>".format(url=value))


def format_datetime(view, context, model, name):
    value = getattr(model, name)
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")


def format_comments(view, context, model, name):
    value = getattr(model, name)
    out = ""

    if isinstance(value, InstrumentedList):
        out = "<ul>"
        for x in value:
            if hasattr(x, "admin_view_link"):
                out += "<li>{commenttitle} {commentcontent}<a href='{commentadminlink}'> Read more...</a></li>".format(
                    commentadminlink=getattr(x, "admin_view_link")(), commenttitle=x.name, commentcontent=x.content)
            else:
                out += str(x)
        out += "</ul>"
    return Markup(out)


formatters = dict(list(zip(["telephones", "users", "contacts", "organizations", "projects",  "deals", "sprints",
                            "links", "tasks", "messages"], cycle([format_instrumented_list]))), comments=format_comments, url=format_url)

formatters = {**formatters, **
              dict(list(zip(["created_at", "updated_at", "closed_at", "start_date", "deadline", "eta"], cycle([format_datetime]))))}


class EnhancedModelView(ModelView):
    can_view_details = True
    column_formatters = formatters


class TelephoneModelView(EnhancedModelView):
    column_filters = column_list = column_details_list = (
        'number', 'contact', 'company')
    column_searchable_list = ('number',)


class ContactModelView(EnhancedModelView):
    column_filters = column_details_list = ('firstname', 'lastname', 'email', 'description', 'telephones', 'message_channels',
                                            'deals', 'comments', 'tasks', 'projects', 'messages', 'sprints', 'links', 'owner', 'ownerbackup')

    column_list = column_filters = (
        'firstname', 'lastname', 'email', 'description', 'telephones', 'message_channels',)
    column_searchable_list = ('firstname', 'lastname', 'email')


class CompanyModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'description', 'email', 'telephones',
                                            'deals', 'messages', 'tasks', 'comments', 'owner', 'ownerbackup')
    column_searchable_list = ('name', 'description', 'email')
    column_list = ('name', 'description', 'email', 'telephones')


class OrganizationModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'email', 'description', 'users', 'tasks', 'comments',
                                            'links', 'messages', 'sprints', 'promoter', 'gaurdian', 'owner')
    column_list = ('name', 'email', 'description', 'owner')
    column_searchable_list = ('name', 'email', 'description',)


class DealModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'remarks', 'amount', 'currency', 'deal_type',
                                            'deal_state', 'tasks', 'comments', 'messages', 'links', 'contact', 'company', 'owner', 'ownerbackup')

    columns_list = ('name', 'amount', 'currency', 'deal_type', 'deal_state')
    column_searchable_list = (
        'name', 'amount', 'currency', 'deal_type', 'deal_state')


class ProjectModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'description', 'start_date', 'deadline', 'comments',
                                            'links', 'tasks', 'sprint', 'messages', 'users', 'promoter', 'gaurdian', 'parent')

    column_list = ('name', 'description', 'start_date', 'deadline', )
    column_searchable_list = ('name', 'description', 'start_date', 'deadline')


class SprintModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'description', 'start_date', 'deadline', 'comments',
                                            'links', 'tasks', 'messages', 'users', 'promoter', 'gaurdian', 'parent')
    column_list = ('name', 'description', 'start_date', 'deadline')
    column_searchable_list = ('name', 'description', 'start_date', 'deadline')


class CommentModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'remarks', 'content', 'company', 'contact', 'organization', 'task', 'project',
                                            'link', 'deal', 'sprint')
    column_list = ('name', 'content')
    column_searchable_list = ('name', 'content')


class LinkModelView(EnhancedModelView):
    column_filters = column_details_list = ('url', 'labels', 'contact', 'organization', 'task', 'project',
                                            'deal', 'sprint', 'comments')
    column_list = ('url', 'labels')
    column_searchable_list = ('url', 'labels')


class TaskModelView(EnhancedModelView):
    column_filters = column_details_list = ('title', 'description', 'remarks', 'content', 'type', 'priority', 'eta', 'time_done',
                                            'assignee', 'company', 'deal', 'organization', 'project', 'sprint', 'comments', 'messages')
    column_list = ('title', 'description', 'assignee',
                   'organization', 'deal', 'project', 'sprint')
    column_searchable_list = ('title', 'description',
                              'content', 'type', 'priority', 'eta')


class MessageModelView(EnhancedModelView):
    column_filters = column_details_list = ('title', 'content', 'channel', 'time_tosend', 'time_sent',
                                            'company', 'contact', 'deal', 'organization', 'task', 'project', 'sprint')
    column_list = ('title', 'content', 'channel', 'time_tosend', 'time_sent',
                   'company', 'contact', 'deal', 'organizaton', 'task', 'project', 'sprint')
    column_searchable_list = ('title', 'content', 'channel')
