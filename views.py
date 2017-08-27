from itertools import cycle
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm.collections import InstrumentedList
from flask_admin.model import typefmt
from jinja2 import Markup


def format_instrumented_list(view, context, model, name):
    value = getattr(model, name)
    out = ""

    if isinstance(value, InstrumentedList):
        print("\n\n////////NAME ", name, " VALUE: ", value, "\n\n")
        for x in value:
            if hasattr(x, "admin_view_link"):
                out += Markup("<a href='{}'>{}</a> ".format(
                    getattr(x, "admin_view_link")(), x))
            else:
                out += str(x)
    return out

formatters = dict(list(zip(["telephones", "comments", "contacts", "projects", "deals", "sprints",
                            "links", "comments",
                            "tasks", "messages"], cycle([format_instrumented_list]))))


class EnhancedModelView(ModelView):
    can_view_details = True
    column_formatters = formatters


class TelephoneModelView(EnhancedModelView):
    column_details_list = ('number', 'contact')


class ContactModelView(EnhancedModelView):
    column_details_list = ('firstname', 'lastname', 'email', 'description', 'telephones',
                           'organizations', 'deals', 'comments', 'tasks', 'messages', 'links', 'owner', 'ownerbackup')


class CompanyModelView(EnhancedModelView):
    column_details_list = ('name', 'description', 'email', 'telephones',
                           'deals', 'messages', 'tasks', 'comments', 'owner', 'ownerbackup')


class OrganizationModelView(EnhancedModelView):
    column_details_list = ('name', 'email', 'description', 'users', 'tasks', 'comments',
                           'links', 'messages', 'sprints', 'promoter', 'gaurdian', 'parent', 'owner')


class DealModelView(EnhancedModelView):
    column_details_list = ('name', 'remarks', 'amount', 'currency', 'deal_type',
                           'deal_state', 'tasks', 'comments', 'messages', 'links', 'contact', 'owner', 'ownerbackup')


class ProjectModelView(EnhancedModelView):
    column_details_list = ('name', 'description', 'start_date', 'deadline', 'comments',
                           'links', 'tasks', 'sprint', 'messages', 'users', 'promoter', 'gaurdian')


class SprintModelView(EnhancedModelView):
    column_details_list = ('name', 'description', 'start_date', 'deadline', 'comments',
                           'links', 'tasks', 'messages', 'users', 'promoter', 'gaurdian', 'parent')


class CommentModelView(EnhancedModelView):
    column_details_list = ('name', 'remarks', 'content', 'company', 'organization', 'task', 'project',
                           'link', 'deal', 'sprint')


class LinkModelView(EnhancedModelView):
    column_details_list = ('url', 'labels', 'contact', 'organization', 'task', 'project',
                           'deal', 'sprint')


class TaskModelView(EnhancedModelView):
    column_details_list = ('title', 'description', 'remarks', 'content', 'type', 'priority', 'eta', 'time_done',
                           'company', 'deal', 'organization', 'project', 'sprint', 'comments', 'messages')


class MessageModelView(EnhancedModelView):
    column_details_list = ('title', 'content', 'channel', 'time_tosend', 'time_sent',
                           'company', 'contact', 'deal', 'organization', 'task', 'project', 'sprint')
