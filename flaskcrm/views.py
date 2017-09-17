from itertools import cycle
from flask_admin.contrib.sqla import ModelView
import sqlalchemy
import flask_admin
from flask_admin.model import typefmt
from flask_admin.base import expose
from models import db, Telephone as TelephoneModel, Email as EmailModel, User as UserModel, Contact as ContactModel, Company as CompanyModel, Organization as OrganizationModel, Deal as DealModel, Deal as DealModel, Link as LinkModel, Project as ProjectModel, Sprint as SprintModel, Task as TaskModel, Comment as CommentModel, Message as MessageModel
from formatters import column_formatters
from converters import CustomAdminConverter
from flask_admin.contrib.sqla.tools import is_relationship
from flask_admin.contrib.sqla import form, filters as sqla_filters, tools
from flask_admin._compat import string_types, text_type


class EnhancedModelView(ModelView):
    can_view_details = True
    column_formatters = column_formatters
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
    column_labels = {
        'short_description': 'Description'
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

    def scaffold_filters(self, name):
        """
            Return list of enabled filters
        """
        # if :
        #     import ipdb; ipdb.set_trace()

        attr, joins = tools.get_field_with_path(self.model, name)

        if attr is None:
            raise Exception('Failed to find field for filter: %s' % name)

        # Figure out filters for related column
        if is_relationship(attr):
            filters = []

            for p in self._get_model_iterator(attr.property.mapper.class_):
                if hasattr(p, 'columns'):
                    # TODO: Check for multiple columns
                    column = p.columns[0]

                    if column.foreign_keys:
                        continue

                    visible_name = '%s / %s' % (self.get_column_name(attr.prop.table.name),
                                                self.get_column_name(p.key))

                    type_name = type(column.type).__name__
                    flt = self.filter_converter.convert(type_name,
                                                        column,
                                                        visible_name)

                    if flt:
                        table = column.table

                        if joins:
                            self._filter_joins[column] = joins
                        elif tools.need_join(self.model, table):
                            self._filter_joins[column] = [table]

                        filters.extend(flt)

            return filters
        else:
            is_hybrid_property = tools.is_hybrid_property(self.model, name)
            if is_hybrid_property:
                column = attr
                if isinstance(name, string_types):
                    column.key = name.split('.')[-1]
            else:
                columns = tools.get_columns_for_field(attr)

                if len(columns) > 1:
                    raise Exception(
                        'Can not filter more than on one column for %s' % name)

                column = columns[0]

            # If filter related to relation column (represented by
            # relation_name.target_column) we collect here relation name
            joined_column_name = None
            if isinstance(name, string_types) and '.' in name:
                joined_column_name = name.split('.')[0]

            # Join not needed for hybrid properties
            if (not is_hybrid_property and tools.need_join(self.model, column.table) and
                    name not in self.column_labels):
                if joined_column_name:
                    visible_name = '%s / %s / %s' % (
                        joined_column_name,
                        self.get_column_name(column.table.name),
                        self.get_column_name(column.name)
                    )
                else:
                    visible_name = '%s / %s' % (
                        self.get_column_name(column.table.name),
                        self.get_column_name(column.name)
                    )
            else:
                if not isinstance(name, string_types):
                    visible_name = self.get_column_name(name.property.key)
                else:
                    if self.column_labels and name in self.column_labels:
                        visible_name = self.column_labels[name]
                    else:
                        visible_name = self.get_column_name(name)
                        visible_name = visible_name.replace('.', ' / ')

            type_name = type(column.type).__name__

            flt = self.filter_converter.convert(
                type_name,
                column,
                visible_name,
                options=self.column_choices.get(name),
            )

            key_name = column
            # In case of filter related to relation column filter key
            # must be named with relation name (to prevent following same
            # target column to replace previous)
            if joined_column_name:
                key_name = "{0}.{1}".format(joined_column_name, column)
                for f in flt:
                    f.key_name = key_name

            if joins:
                self._filter_joins[key_name] = joins
            elif not is_hybrid_property and tools.need_join(self.model, column.table):
                self._filter_joins[key_name] = [column.table]

            return flt


class TelephoneModelView(EnhancedModelView):
    column_list = column_details_list = (
        'number', 'contact', 'company',)

    column_filters = (
        'number', 'contact', 'company', 'user')
    column_searchable_list = ('number',)
    column_sortable_list = ('number',)


class EmailModelView(EnhancedModelView):
    form_rules = column_filters = column_list = column_details_list = (
        'email', 'contact', 'company', 'organization', 'user')
    column_searchable_list = ('email',)
    column_sortable_list = ('email', )


class UserModelView(EnhancedModelView):
    column_list = ('firstname', 'lastname', 'emails',
                   'telephones',)
    form_rules = column_details_list = ('firstname', 'lastname', 'emails', 'telephones', 'description', 'message_channels',
                                        'ownsContacts', 'ownsAsBackupContacts', 'ownsCompanies', 'ownsAsBackupCompanies',
                                        'ownsOrganizations', 'ownsSprints', 'promoterProjects', 'guardianProjects', 'comments', 'messages', 'links',)

    column_filters = ('firstname', 'lastname')
    form_edit_rules = ('firstname', 'lastname', 'description',
                       'emails', 'telephones', 'message_channels', 'messages')
    column_sortable_list = ('firstname', 'lastname')
    column_searchable_list = ('firstname', 'lastname')

    inline_models = [
        (TelephoneModel, {'form_columns': ['id', 'number']}),
        (EmailModel, {'form_columns': ['id', 'email']}),
        (MessageModel, {'form_columns': ['id', 'title', 'channel']}),
        (CommentModel, {'form_columns': ['id', 'content']})]
    mainfilter = "Users / Id"


class ContactModelView(EnhancedModelView):
    form_rules = column_details_list = ('firstname', 'lastname', 'description', 'emails', 'telephones', 'message_channels',
                                        'deals', 'comments', 'tasks', 'projects', 'messages', 'sprints', 'links', 'owner', 'ownerbackup')
    form_edit_rules = ('firstname', 'lastname', 'description', 'emails', 'telephones', 'tasks', 'deals', 'messages', 'comments',
                       'message_channels', 'owner', 'ownerbackup')

    column_filters = ('firstname', 'lastname', 'description', 'emails', 'telephones', 'message_channels',
                      'deals', 'comments', 'tasks', 'projects', 'messages', 'sprints', 'links', 'owner', 'ownerbackup')
    column_searchable_list = ('firstname', 'lastname',)
    column_list = ('firstname', 'lastname', 'emails',
                   'telephones', 'short_description')

    column_sortable_list = ('firstname', 'lastname')

    inline_models = [
        (TelephoneModel, {'form_columns': ['id', 'number']}),
        (EmailModel, {'form_columns': ['id', 'email']}),
        (TaskModel, {'form_columns': [
         'id', 'title', 'description', 'type', 'priority']}),
        (MessageModel, {'form_columns': ['id', 'title', 'channel']}),
        (DealModel, {'form_columns': [
         'id', 'name', 'amount', 'currency', 'deal_type']}),
        (CommentModel, {'form_columns': ['id', 'content']})]

    form_args = {
        'ownerbackup': {'label': 'Backup Owner'},
    }

    mainfilter = "Contacts / Id"


class CompanyModelView(EnhancedModelView):
    form_rules = column_filters = column_details_list = ('name', 'description', 'emails', 'telephones',
                                                         'deals', 'messages', 'tasks', 'comments', 'owner', 'ownerbackup')

    form_edit_rules = ('name', 'description', 'emails', 'telephones', 'messages', 'tasks', 'deals',
                       'comments', 'owner', 'ownerbackup')

    column_searchable_list = ('id', 'name', 'description',)
    column_list = ('name', 'short_description')
    column_sortable_list = ('name', )

    inline_models = [
        (TelephoneModel, {'form_columns': ['id', 'number']}), (EmailModel, {
            'form_columns': ['id', 'email']}),
        (TaskModel, {'form_columns': [
         'id', 'title', 'description', 'type', 'priority', ]}),
        (MessageModel, {'form_columns': ['id', 'title', 'channel']}),
        (DealModel, {'form_columns': [
         'id', 'name', 'amount', 'currency', 'deal_type', 'description', ]}),
        (CommentModel, {'form_columns': ['id', 'content']})]

    mainfilter = "Companies / Id"


class OrganizationModelView(EnhancedModelView):
    form_rules = column_filters = column_details_list = ('name', 'description', 'emails', 'owner',
                                                         'tasks', 'users', 'comments', 'messages',
                                                         'links',)
    form_rules = ('name', 'description', 'emails', 'owner',)

    form_edit_rules = ('name', 'description', 'emails',
                       'owner', 'tasks')

    column_list = ('name', 'emails', 'short_description', 'owner')
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
    mainfilter = "Organizations / Id"


class DealModelView(EnhancedModelView):
    column_filters = column_details_list = ('id', 'name',  'amount', 'currency', 'deal_type', 'deal_state',
                                            'contact', 'company', 'messages')

    form_rules = ('name',  'amount', 'currency', 'deal_type', 'deal_state',
                  'contact', 'company', 'comments',)

    form_edit_rules = ('name',  'amount', 'currency', 'deal_type', 'deal_state',
                       'contact', 'company', 'tasks', 'messages', 'comments')

    column_list = ('name', 'amount', 'currency',
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
                                            'promoter', 'sprints', 'tasks', 'messages', 'guardian')
    form_rules = ('name', 'description', 'start_date', 'deadline',
                  'promoter', 'sprints', 'tasks', 'guardian',)

    form_edit_rules = ('name', 'description',
                       'start_date', 'deadline',
                       'promoter', 'guardian',
                       'tasks', 'messages', 'comments')

    column_list = ('name', 'short_description', 'start_date', 'deadline', )
    column_searchable_list = (
        'id', 'name', 'description', 'start_date', 'deadline')
    column_sortable_list = ('name', 'start_date', 'deadline')

    inline_models = [
        (TaskModel, {'form_columns': [
         'id', 'title', 'type', 'priority', ]}),
        (MessageModel, {'form_columns': ['id', 'title', 'content']}),
        (CommentModel, {'form_columns': ['id', 'content']})
    ]
    mainfilter = "Projects / Id"


class SprintModelView(EnhancedModelView):
    column_filters = column_details_list = ('id', 'name', 'description', 'start_date', 'deadline',
                                            'project', 'contacts',
                                            'comments', 'links', 'messages', )
    form_rules = ('name', 'description', 'start_date', 'deadline',
                  'project',
                  )

    form_edit_rules = ('name', 'description', 'start_date', 'deadline',
                       'project', 'contacts', 'tasks', 'messages', 'comments')
    column_list = ('name', 'short_description', 'start_date', 'deadline')
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

    mainfilter = "Sprints / Id"


class CommentModelView(EnhancedModelView):
    column_filters = column_details_list = ('id', 'content',
                                            'company', 'contact', 'user', 'organization', 'project', 'sprint', 'task',
                                            'link', 'deal', 'sprint')
    form_rules = ('content',
                  'company', 'contact', 'organization', 'project', 'sprint', 'task',
                  'link', 'deal', 'sprint')
    form_edit_rules = ('content',)
    column_list = ('id', 'content')
    column_searchable_list = ('id', 'content')
    column_sortable_list = ('content',)


class LinkModelView(EnhancedModelView):
    column_filters = column_details_list = ('url', 'contact', 'user', 'organization', 'task', 'project',
                                            'deal', 'sprint', 'labels', 'comments')
    form_rules = ('url', 'contact', 'organization', 'task', 'project',
                  'deal', 'sprint', 'labels',)
    form_edit_rules = ('url', 'labels')
    column_list = ('url', 'labels')
    column_searchable_list = ('id', 'url', 'labels')
    column_sortable_list = ('url', )


class TaskModelView(EnhancedModelView):
    column_details_list = ('id', 'title', 'description', 'contact',
                           'type', 'priority', 'eta', 'state', 'time_done',
                           'company', 'organization', 'project', 'sprint', 'deal',
                           'comments', 'messages')

    column_filters = ('id', 'title', 'description', 'contact',
                      'type', 'priority', 'eta', 'time_done',
                      'company', 'organization', 'project', 'sprint', 'deal',
                      'comments', 'messages')
    form_rules = ('title', 'description',
                  'type', 'priority', 'eta', 'time_done',
                  'contact', 'company', 'organization', 'project', 'sprint', 'deal')

    form_edit_rules = ('title', 'description', 'contact', 'state',
                       'type', 'priority', 'time_done', 'comments', 'messages')
    column_list = ('title', 'type', 'priority',
                   'organization', 'company', 'project', 'sprint', 'deal')
    column_searchable_list = ('id', 'title', 'description',
                              'type', 'priority')
    column_sortable_list = (['priority'])

    inline_models = [
        (CommentModel, {'form_columns': [
         'id', 'content', ]}),
        (MessageModel, {'form_columns': [
         'id', 'title', 'content', 'channel']}),
    ]
    form_args = {
        'contact': {
            'label': 'Assignee',
        }
    }


class MessageModelView(EnhancedModelView):
    form_rules = column_filters = ('title', 'content', 'channel', 'time_tosend', 'time_sent',
                                   'company', 'contact', 'user', 'organization', 'project', 'sprint', 'deal', 'task')
    column_details_list = ('id', 'title', 'author', 'content', 'company',
                           'contact', 'organization', 'project', 'sprint', 'deal', 'task')

    form_edit_rules = ('title', 'author', 'content', 'channel',
                       'time_tosend', 'time_sent',)
    column_list = ('author', 'title', 'content',
                   'company', 'contact', 'deal', 'organizaton', 'task', 'project', 'sprint')
    column_searchable_list = ('title', 'content')
    column_sortable_list = ('title', 'author')


class TaskAssignmentModelView(EnhancedModelView):
    column_details_list = ('contact', 'task', 'tasktracking')
    column_list = ('percent_completed', 'contact',
                   'task',)


class TaskTrackingModelView(EnhancedModelView):
    column_list = column_details_list = ('remarks',
                                         'time_done',)
