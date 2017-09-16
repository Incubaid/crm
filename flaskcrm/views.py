from itertools import cycle
from flask_admin.contrib.sqla import ModelView
import sqlalchemy
from sqlalchemy.orm.collections import InstrumentedList
import flask_admin
from flask_admin.model import typefmt
from flask_admin.base import expose
from flask_admin.form.fields import Select2Field
from flask_admin.model.form import converts
from flask_misaka import markdown
from jinja2 import Markup
from datetime import datetime
from models import db, Telephone as TelephoneModel, Email as EmailModel, Contact as ContactModel, Company as CompanyModel, Organization as OrganizationModel, Deal as DealModel, Deal as DealModel, Link as LinkModel, Project as ProjectModel, Sprint as SprintModel, Task as TaskModel, Comment as CommentModel, Message as MessageModel


def format_instrumented_list(view, context, model, name):

    value = getattr(model, name)
    out = ""
    if isinstance(value, InstrumentedList):
        out = "<ul>"
        for x in value:
            if x is None:  # items can be created from empty forms in the form. let's fix that in the model
                continue
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
                out += "<li>{commentcontent}<a href='{commentadminlink}'> Read more...</a></li>".format(
                    commentadminlink=getattr(x, "admin_view_link")(), commentcontent=x.content)
            else:
                out += str(x)
        out += "</ul>"
    return Markup(out)


def format_description(view, context, model, name):
    value = getattr(model, name)
    if value:
        return markdown(value)
    return value

def format_emails(view, context, model, name):
    value = getattr(model, name)
    out = "<ul>" 
    for x in value:
        out += '<li><a href="mailto:{email}">{email}</a></li>'.format(email=x)
    out += "</ul>"
    return Markup(out)


formatters = dict(list(zip(["telephones", "users", "contacts", "organizations", "projects",  "deals", "sprints",
                            "links", "tasks", "messages"], cycle([format_instrumented_list]))), comments=format_comments, url=format_url, emails=format_emails, description=format_description)

formatters = {**formatters, **
              dict(list(zip(["created_at", "updated_at", "closed_at", "start_date", "deadline", "eta"], cycle([format_datetime]))))}

class EnumField(Select2Field):
    def __init__(self, column, **kwargs):
        assert isinstance(column.type, sqlalchemy.sql.sqltypes.Enum)

        def coercer(value):
            # coerce incoming value into an enum value
            if isinstance(value, column.type.enum_class):
                return value
            elif isinstance(value, str):
                return column.type.enum_class[value]
            else:
                assert False

        super(EnumField, self).__init__(
            choices=[(v, v) for v in column.type.enums],
            coerce=coercer,
            **kwargs)

    def pre_validate(self, form):
        # we need to override the default SelectField validation because it
        # apparently tries to directly compare the field value with the choice
        # key; it is not clear how that could ever work in cases where the
        # values and choice keys must be different types

        for (v, _) in self.choices:
            if self.data == self.coerce(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class CustomAdminConverter(flask_admin.contrib.sqla.form.AdminModelConverter):
    @converts("sqlalchemy.sql.sqltypes.Enum")
    def conv_enum(self, field_args, **extra):
        return EnumField(column=extra["column"], **field_args)

class EnhancedModelView(ModelView):
    can_view_details = True
    column_formatters = formatters
    create_modal = True
    edit_modal = True
    model_form_converter = CustomAdminConverter
    mainfilter = ""

    form_widget_args = {
        'created_at': {
            'readonly': True,
        },
        'updated_at': {
            'readonly': True,
        },
    }

    def get_filter_arg_helper(self, filter_name, filter_op='equals'):
        filters = self._filter_groups[filter_name].filters
        position = list(self._filter_groups.keys()).index(filter_name)

        for f in filters:
            if f['operation'] == filter_op:
                return 'flt%d_%d' % (position, f['index'])

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        if self.mainfilter:
            filtered_objects = {}
            filtered_objects['emailsview'] = [
                EmailModelView(EmailModel, db.session), self.mainfilter]
            filtered_objects['telephonesview'] = [
                TelephoneModelView(TelephoneModel, db.session), self.mainfilter]
            filtered_objects['tasksview'] = [
                TaskModelView(TaskModel, db.session), self.mainfilter]
            filtered_objects['messagesview'] = [MessageModelView(
                MessageModel, db.session), self.mainfilter]
            filtered_objects['projectsview'] = [ProjectModelView(
                ProjectModel, db.session), self.mainfilter]
            filtered_objects['sprintsview'] = [SprintModelView(
                SprintModel, db.session), self.mainfilter]
            filtered_objects['dealsview'] = [DealModelView(
                DealModel, db.session), self.mainfilter]
            filtered_objects['commentsview'] = [CommentModelView(
                CommentModel, db.session), self.mainfilter]
            filtered_objects['linksview'] = [LinkModelView(
                LinkModel, db.session), self.mainfilter]

            self._template_args['filtered_objects'] = filtered_objects
        return super().edit_view()

    @expose('/details/', methods=('GET',))
    def details_view(self):
        if self.mainfilter:
            filtered_objects = {}
            filtered_objects['emailsview'] = [
                EmailModelView(EmailModel, db.session), self.mainfilter]
            filtered_objects['telephonesview'] = [
                TelephoneModelView(TelephoneModel, db.session), self.mainfilter]
            filtered_objects['tasksview'] = [
                TaskModelView(TaskModel, db.session), self.mainfilter]
            filtered_objects['messagesview'] = [MessageModelView(
                MessageModel, db.session), self.mainfilter]
            filtered_objects['projectsview'] = [ProjectModelView(
                ProjectModel, db.session), self.mainfilter]
            filtered_objects['sprintsview'] = [SprintModelView(
                SprintModel, db.session), self.mainfilter]
            filtered_objects['dealsview'] = [DealModelView(
                DealModel, db.session), self.mainfilter]
            filtered_objects['commentsview'] = [CommentModelView(
                CommentModel, db.session), self.mainfilter]
            filtered_objects['linksview'] = [LinkModelView(
                LinkModel, db.session), self.mainfilter]

            self._template_args['filtered_objects'] = filtered_objects
        return super().details_view()


def possible_owners():
    return ContactModel.query.filter(
        ContactModel.isemployee == True).all()


class TelephoneModelView(EnhancedModelView):
    column_list = column_details_list = (
        'number', 'contact', 'company',)

    column_filters = (
        'number', 'contact', 'company',)
    column_searchable_list = ('number',)
    column_sortable_list = ('number',)


class EmailModelView(EnhancedModelView):
    form_rules = column_filters = column_list = column_details_list = (
        'email', 'contact', 'company', 'organization')
    column_searchable_list = ('email',)
    column_sortable_list = ('email', )


class ContactModelView(EnhancedModelView):
    form_rules = column_details_list = ('firstname', 'lastname', 'description', 'emails', 'telephones', 'message_channels',
                                        'deals', 'comments', 'tasks', 'projects', 'messages', 'sprints', 'isemployee', 'links', 'owner', 'ownerbackup')
    form_edit_rules = ('firstname', 'lastname', 'description', 'emails', 'telephones', 'tasks', 'deals', 'comments',
                       'message_channels', 'isemployee', 'owner', 'ownerbackup')

    column_filters = ('firstname', 'lastname', 'description', 'emails', 'telephones', 'message_channels',
                      'deals', 'comments', 'tasks', 'projects', 'messages', 'sprints', 'links', 'owner', 'ownerbackup')
    column_searchable_list = ('firstname', 'lastname',)
    column_list = ('firstname', 'lastname', 'emails',
                   'telephones', 'description')

    column_sortable_list = ('firstname', 'lastname')

    inline_models = [
        (TelephoneModel, {'form_columns': ['id', 'number']}),
        (EmailModel, {'form_columns': ['id', 'email']}),
        (TaskModel, {'form_columns': [
         'id', 'title', 'description', 'type', 'priority']}),
        (DealModel, {'form_columns': [
         'id', 'name', 'amount', 'currency', 'deal_type']}),
        (CommentModel, {'form_columns': ['id', 'content']})]

    form_args = {
        'isemployee': {'label': 'Employee?'},
        'owner': {'query_factory': possible_owners},
        'ownerbackup': {'query_factory': possible_owners, 'label': 'Backup Owner'},
    }

    mainfilter = "Contacts / Uid"


class CompanyModelView(EnhancedModelView):
    form_rules = column_filters = column_details_list = ('name', 'description', 'emails', 'telephones',
                                                         'deals', 'messages', 'tasks', 'comments', 'owner', 'ownerbackup')

    form_edit_rules = ('name', 'description', 'emails', 'telephones', 'messages', 'tasks', 'deals',
                       'comments', 'owner', 'ownerbackup')

    column_searchable_list = ('id', 'name', 'description',)
    column_list = ( 'name', 'description')
    column_sortable_list = ('name', )

    inline_models = [
        (TelephoneModel, {'form_columns': ['id', 'number']}), (EmailModel, {
            'form_columns': ['id', 'email']}),
        (TaskModel, {'form_columns': [
         'id', 'title', 'description', 'type', 'priority', ]}),
        (MessageModel, {'form_columns': ['id', 'title', 'channel']}),
        (DealModel, {'form_columns': [
         'id', 'name', 'amount', 'currency', 'deal_type', 'remarks', ]}),
        (CommentModel, {'form_columns': ['id', 'content']})]

    mainfilter = "Companies / Uid"


class OrganizationModelView(EnhancedModelView):
    form_rules = column_filters = column_details_list = ('name', 'description', 'emails', 'owner',
                                                         'tasks', 'users', 'comments',
                                                         'links',)
    form_rules = ('name', 'description', 'emails', 'owner',)

    form_edit_rules = ('name', 'description', 'emails',
                       'owner', 'tasks')

    column_list = ('name', 'emails', 'description', 'owner')
    column_searchable_list = ('id', 'name', 'description',)
    column_sortable_list = ('name',)

    inline_models = [
        (EmailModel, {
            'form_columns': ['id', 'email']}),
        (TaskModel, {'form_columns': [
         'id', 'title', 'type', 'priority', ]}),
        (MessageModel, {'form_columns': ['id', 'title', 'content', 'channel']},
         (CommentModel, {'form_columns': ['id', 'content']}))
    ]
    mainfilter = "Organizations / Uid"


class DealModelView(EnhancedModelView):
    column_filters = column_details_list = ('id', 'name',  'amount', 'currency', 'deal_type', 'deal_state',
                                            'contact', 'company')

    form_rules = ('name',  'amount', 'currency', 'deal_type', 'deal_state',
                  'contact', 'company', 'owner', 'ownerbackup',
                  'comments',)

    form_edit_rules = ('name',  'amount', 'currency', 'deal_type', 'deal_state',
                       'contact', 'company', 'owner', 'ownerbackup', 'tasks', 'messages', 'comments')

    column_list = ( 'name', 'amount', 'currency',
                   'deal_type', 'deal_state')
    column_searchable_list = (
        'id', 'name', 'amount', 'currency', 'deal_type', 'deal_state')

    column_sortable_list = ('name', 'amount', 'currency',
                            'deal_type', 'deal_state')

    inline_models = [
        (TaskModel, {'form_columns': [
         'id', 'title', 'type', 'priority', ]}),
        (MessageModel, {'form_columns': ['id', 'title', 'content']}),
        (CommentModel, {'form_columns': ['id', 'content']})
    ]


class ProjectModelView(EnhancedModelView):
    column_filters = column_details_list = ('name', 'description', 'start_date', 'deadline',
                                            'promoter', 'sprint', 'tasks', 'guardian')
    form_rules = ('name', 'description', 'start_date', 'deadline',
                  'promoter', 'sprint', 'tasks', 'guardian',)

    edit_form_rules = ('name', 'description',
                       'start_date', 'deadline',
                       'promoter', 'guardian',
                       'users', 'tasks', 'messages', 'comments')

    column_list = ( 'name', 'description', 'start_date', 'deadline', )
    column_searchable_list = (
        'id', 'name', 'description', 'start_date', 'deadline')
    column_sortable_list = ('name', 'start_date', 'deadline')

    inline_models = [
        (TaskModel, {'form_columns': [
         'id', 'title', 'description', 'type', 'priority', ]}),
        (MessageModel, {'form_columns': ['id', 'title', 'content', 'channel']},
         (CommentModel, {'form_columns': ['id', 'content']}))
    ]

    mainfilter = "Projects / Uid"


class SprintModelView(EnhancedModelView):
    column_filters = column_details_list = ('id', 'name', 'description', 'start_date', 'deadline',
                                            'promoter', 'guardian', 'parent', 'users',
                                            'comments', 'links', 'messages', )
    form_rules = ('name', 'description', 'start_date', 'deadline',
                  'promoter', 'guardian', 'parent',
                  )

    form_edit_rules = ('name', 'description', 'start_date', 'deadline',
                       'promoter', 'guardian', 'parent', 'users', 'tasks', 'messages', 'comments')
    column_list = ('name', 'description', 'start_date', 'deadline')
    column_searchable_list = (
        'id', 'name', 'description', 'start_date', 'deadline')
    column_sortable_list = ('name', 'start_date', 'deadline')

    inline_models = [
        (TaskModel, {'form_columns': [
         'id', 'title', 'type', 'priority', ]}),
        (MessageModel, {'form_columns': [
         'id', 'title', 'content', 'channel']}),
        (CommentModel, {'form_columns': ['id', 'content']})
    ]

    mainfilter = "Sprints / Uid"


class CommentModelView(EnhancedModelView):
    column_filters = column_details_list = ('id', 'content',
                                            'company', 'contact', 'organization', 'project', 'sprint', 'task',
                                            'link', 'deal', 'sprint')
    form_rules = ('content',
                  'company', 'contact', 'organization', 'project', 'sprint', 'task',
                  'link', 'deal', 'sprint')
    form_edit_rules = ('content')
    column_list = ('id', 'content')
    column_searchable_list = ('id', 'content')
    column_sortable_list = ('content',)


class LinkModelView(EnhancedModelView):
    column_filters = column_details_list = ('url', 'contact', 'organization', 'task', 'project',
                                            'deal', 'sprint', 'labels', 'comments')
    form_rules = ('url', 'contact', 'organization', 'task', 'project',
                  'deal', 'sprint', 'labels',)
    form_edit_rules = ('url', 'labels')
    column_list = ('url', 'labels')
    column_searchable_list = ('id', 'url', 'labels')
    column_sortable_list = ('url', )


class TaskModelView(EnhancedModelView):
    column_details_list = ('id', 'title', 'description', 'contacts',
                           'type', 'priority', 'eta', 'time_done',
                           'company', 'organization', 'project', 'sprint', 'deal',
                           'comments', 'messages')

    column_filters = ('id', 'title', 'description', 'contacts',
                      'type', 'priority', 'eta', 'time_done',
                      'company', 'organization', 'project', 'sprint', 'deal',
                      'comments', 'messages')
    form_rules = ('title', 'description',
                  'type', 'priority', 'eta', 'time_done',
                  'contacts', 'company', 'organization', 'project', 'sprint', 'deal')

    form_edit_rules = ('title', 'description',
                       'type', 'priority', 'time_done', 'comments')
    column_list = ('title', 'type', 'priority',
                   'organization', 'company', 'project', 'sprint', 'deal')
    column_searchable_list = ('id', 'title', 'description',
                              'type', 'priority')
    column_sortable_list = (['priority'])

    inline_models = [
        (CommentModel, {'form_columns': [
         'id', 'content', ]}),
    ]


class MessageModelView(EnhancedModelView):
    form_rules = column_filters = ('title', 'content', 'channel', 'time_tosend', 'time_sent',
                                   'company', 'contact', 'organization', 'project', 'sprint', 'deal', 'task')
    column_details_list = ('id', 'title', 'content', 'company',
                           'contact', 'organization', 'project', 'sprint', 'deal', 'task')

    form_edit_rules = ('title', 'content', 'channel',
                       'time_tosend', 'time_sent',)
    column_list = ('title', 'content',
                   'company', 'contact', 'deal', 'organizaton', 'task', 'project', 'sprint')
    column_searchable_list = ('title', 'content')
    column_sortable_list = ('title',)


class TaskAssignmentModelView(EnhancedModelView):
    column_details_list = ('contact', 'task', 'tasktracking')
    column_list = ('percent_completed', 'contact',
                   'task',)


class TaskTrackingModelView(EnhancedModelView):
    column_list = column_details_list = ('remarks',
                                         'time_done',)
