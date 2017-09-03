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


formatters = dict(list(zip(["telephones", "emails", "users", "contacts", "organizations", "projects",  "deals", "sprints",
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


class EmailModelView(EnhancedModelView):
    column_filters = column_list = column_details_list = (
        'contact', 'company', 'organization')
    column_searchable_list = ('email',)


class ContactModelView(EnhancedModelView):
    column_filters = column_details_list = ('firstname', 'lastname', 'description', 'emails', 'telephones', 'message_channels',
                                            'deals', 'comments', 'tasks', 'projects', 'messages', 'sprints', 'links', 'owner', 'ownerbackup')

    column_list = column_filters = (
        'firstname', 'lastname', 'emails', 'description', 'telephones', 'message_channels',)
    column_searchable_list = ('firstname', 'lastname',)

    form_widget_args = {
        'created_at': {
            'readonly': True,
        },
        'updated_at': {
            'readonly': True,
        },
    }


class CompanyModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'description', 'emails', 'telephones',
                                            'deals', 'messages', 'tasks', 'comments', 'owner', 'ownerbackup')
    column_searchable_list = ('name', 'description',)
    column_list = ('name', 'description', 'emails', 'telephones')


class OrganizationModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'description', 'emails',
                                            'promoter', 'gaurdian', 'owner',
                                            'sprints', 'tasks', 'users', 'messages', 'comments',
                                            'links',)
    column_list = ('name', 'emails', 'description', 'owner')
    column_searchable_list = ('name', 'description',)


class DealModelView(EnhancedModelView):
    column_filters = column_details_list = ('name',  'amount', 'currency', 'deal_type', 'deal_state',
                                            'contact', 'company', 'owner', 'ownerbackup',
                                            'tasks', 'remarks', 'messages', 'comments',
                                            'links', )

    columns_list = ('name', 'amount', 'currency', 'deal_type', 'deal_state')
    column_searchable_list = (
        'name', 'amount', 'currency', 'deal_type', 'deal_state')


class ProjectModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'description', 'start_date', 'deadline',
                                            'promoter', 'sprint', 'tasks', 'gaurdian',
                                            'users', 'comments', 'messages', 'links',)

    column_list = ('name', 'description', 'start_date', 'deadline', )
    column_searchable_list = ('name', 'description', 'start_date', 'deadline')


class SprintModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'description', 'start_date', 'deadline',
                                            'promoter', 'gaurdian', 'parent', 'users',
                                            'comments', 'links', 'tasks', 'messages', )

    column_list = ('name', 'description', 'start_date', 'deadline')
    column_searchable_list = ('name', 'description', 'start_date', 'deadline')


class CommentModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'content',
                                            'company', 'contact', 'organization', 'project', 'sprint', 'task',
                                            'link', 'deal', 'sprint', 'remarks')
    column_list = ('name', 'content')
    column_searchable_list = ('name', 'content')


class LinkModelView(EnhancedModelView):
    column_filters = column_details_list = ('url', 'contact', 'organization', 'task', 'project',
                                            'deal', 'sprint', 'labels', 'comments')
    column_list = ('url', 'labels')
    column_searchable_list = ('url', 'labels')


class TaskModelView(EnhancedModelView):
    column_filters = column_details_list = ('title', 'description', 'content',
                                            'type', 'priority', 'eta', 'time_done',
                                            'assignee', 'company', 'organization', 'project', 'sprint', 'deal',
                                            'comments', 'messages', 'remarks')

    column_list = ('title', 'description', 'assignee',
                   'organization', 'company', 'project', 'sprint', 'deal')
    column_searchable_list = ('title', 'description',
                              'content', 'type', 'priority', 'eta')


class MessageModelView(EnhancedModelView):
    column_filters = column_details_list = ('title', 'content', 'channel', 'time_tosend', 'time_sent',
                                            'company', 'contact', 'organization', 'project', 'sprint', 'deal', 'task')

    column_list = ('title', 'content', 'channel', 'time_tosend', 'time_sent',
                   'company', 'contact', 'deal', 'organizaton', 'task', 'project', 'sprint')
    column_searchable_list = ('title', 'content', 'channel')
