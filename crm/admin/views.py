import os
import uuid
import csv
from io import StringIO
from flask import request
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_admin.base import expose
from flask_admin.contrib.sqla.tools import is_relationship
from flask_admin.contrib.sqla import tools
from flask_admin._compat import string_types
from flask_admin.model.form import InlineFormAdmin
from flask_admin import form
from flask_admin.actions import action
from flask import make_response
from wtforms.fields import StringField
from wtforms.widgets import HTMLString
from wtforms import fields
from crm.address.models import Address as AddressModel
from crm.deal.models import Deal as DealModel
from crm.link.models import Link as LinkModel
from crm.project.models import Project as ProjectModel
from crm.sprint.models import Sprint as SprintModel
from crm.task.models import Task as TaskModel
from crm.message.models import Message as MessageModel
from crm.comment.models import Comment as CommentModel
from crm.contact.models import Contact as ContactModel
from crm.company.models import Company as CompanyModel
from crm.event.models import Event as EventModel
from crm.image.models import Image as ImageModel
from flask import session
from .formatters import column_formatters
from .converters import CustomAdminConverter

from crm.db import db
from crm.settings import IMAGES_DIR


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    mainfilter = "Users / Id"

    @expose('/')
    def index(self):
        if self.mainfilter:
            filtered_objects = {}

            filtered_objects['tasksview'] = [
                TaskModelView(TaskModel, db.session), self.mainfilter]
            filtered_objects['contactsview'] = [
                ContactModelView(ContactModel, db.session), self.mainfilter]
            filtered_objects['ownstasksview'] = [
                TaskModelView(TaskModel, db.session), 'assignee / Users / Id']

            filtered_objects['companiesview'] = [
                CompanyModelView(CompanyModel, db.session), self.mainfilter]
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
            self._template_args['current_user_id'] = session[
                'user']['id'] if 'user' in session else ''

        return super().index()


class EnhancedModelView(ModelView):
    columns_list_extra = ['author_last', 'updated_at']
    can_view_details = True
    can_export = True
    column_formatters = column_formatters
    # create_modal = True
    # edit_modal = True
    model_form_converter = CustomAdminConverter
    mainfilter = ""

    form_widget_args = {
        'created_at': {
            'readonly': True,
        },
        'updated_at': {
            'readonly': True,
        },

        'ownsTasks': {
            'label': 'Tasks assigned',
        },
    }

    column_labels = {
        'short_description': 'Description',
        'short_content': 'Content',
        'vatnumber': 'VAT Number',
        'ownsTasks': 'Tasks assigned',
        'ownsContacts': 'Owns contacts',
        'ownsCompanies': 'Owns companies',
        'ownsAsBackupContacts': 'Owns contacts as backup',
        'ownsAsBackupCompanies': 'Owns companies as backup',
        'ownsOrganizations': 'Owns organizations',
        'ownsSprints': 'Owns sprints',
        'promoterProjects': 'Promotes projects',
        'guardianProjects': 'Guards projects',
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

            filtered_objects['tasksview'] = [
                TaskModelView(TaskModel, db.session), self.mainfilter]
            filtered_objects['contactsview'] = [ContactModelView(
                ContactModel, db.session), self.mainfilter]
            # filtered_objects['eventsview'] = [EventModelView(
            #     EventModel, db.session), self.mainfilter]

            filtered_objects['companiesview'] = [
                CompanyModelView(CompanyModel, db.session), self.mainfilter]
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
            filtered_objects['tasksview'] = [
                TaskModelView(TaskModel, db.session), self.mainfilter]
            filtered_objects['ownstasksview'] = [
                TaskModelView(TaskModel, db.session), 'assignee / Users / Id']
            filtered_objects['contactsview'] = [ContactModelView(
                ContactModel, db.session), self.mainfilter]
            filtered_objects['eventsview'] = [EventModelView(
                EventModel, db.session), self.mainfilter]

            filtered_objects['companiesview'] = [
                CompanyModelView(CompanyModel, db.session), self.mainfilter]
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

    def get_save_return_url(self, model, is_created):
        return self.get_url('.details_view', id=model.id)


class UserModelView(EnhancedModelView):
    column_list = ('firstname', 'lastname', 'username', 'emails',
                   'telephones', *EnhancedModelView.columns_list_extra)

    column_details_list = (
        'firstname', 'lastname', 'username', 'emails', 'telephones', 'description', 'message_channels',
        'ownsContacts', 'ownsTasks', 'tasks', 'ownsAsBackupContacts', 'ownsCompanies', 'ownsAsBackupCompanies',
        'ownsOrganizations', 'ownsSprints', 'promoterProjects', 'guardianProjects', 'comments', 'messages', 'links', 'author_last', 'author_original', 'updated_at')

    column_filters = ('firstname', 'lastname',
                      'username', 'ownsTasks',)
    column_sortable_list = ('firstname', 'lastname', 'username')
    column_searchable_list = ('firstname', 'lastname', 'username')

    form_rules = (
        'firstname', 'lastname', 'username', 'emails', 'telephones', 'description', 'message_channels',)

    form_edit_rules = ('firstname', 'lastname', 'username', 'description',
                       'emails', 'telephones', 'message_channels', 'ownsTasks', 'tasks', 'messages', 'comments', 'links')

    inline_models = [
        (TaskModel, {'form_columns': [
            'id', 'title', 'description', 'type', 'priority', 'assignee', 'eta', 'deadline']}),
        (MessageModel, {'form_columns': [
            'id', 'title', 'content', 'channel']}),
        (CommentModel, {'form_columns': ['id', 'content']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}),
    ]
    mainfilter = "Users / Id"


class ImageModelView(EnhancedModelView):
    column_list = ('name', 'path')
    form_rules = column_details_list = ('name', 'path')
    form_edit_rules = ('name', 'path')
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      IMAGES_DIR,
                                      thumbnail_size=(100, 100, True)),
    }


class ImagePreviewWidget(object):

    def __call__(self, field, **kwargs):
        objpk = kwargs.get('pk', None)
        obj = kwargs.get('obj', None)
        kwargs.setdefault('id', field.id)
        if obj is not None:
            return HTMLString(obj.as_image)
        return ""


class ImagePreviewField(StringField):
    widget = ImagePreviewWidget()


class InlineEventModelForm(InlineFormAdmin):
    form_columns = ('id', 'title', 'contact_event_status')
    form_widget_args = {
        'title': {
            'readonly': True
        }
    }

    def __init__(self,):
        return super(InlineEventModelForm, self).__init__(EventModel)


class InlineImageModelForm(InlineFormAdmin):
    form_excluded_columns = ('path', 'name', 'created_at',
                             'updated_at',)
    form_label = 'Image'

    def __init__(self,):
        return super(InlineImageModelForm, self).__init__(ImageModel)

    def postprocess_form(self, form_class):
        form_class.upload = fields.FileField('Image')
        form_class.preview = ImagePreviewField("")
        return form_class

    def on_model_change(self, form, model):
        file_data = request.files.get(form.upload.name)
        ext = file_data.filename.split('.')[-1]

        if file_data:
            newname = '%s.%s' % (str(uuid.uuid4()), ext)
            model.path = newname
            model.name = file_data.filename
            if not os.path.exists(os.path.join(IMAGES_DIR, newname)):
                file_data.save(os.path.join(IMAGES_DIR, newname))


class SubgroupModelView(EnhancedModelView):
    column_list = ('groupname', *EnhancedModelView.columns_list_extra)
    column_details_list = ('groupname', )
    form_rules = ('groupname', )
    form_edit_rules = ('groupname',)


class TagModelView(EnhancedModelView):
    column_list = ('tag',)
    column_details_list = ('tag', 'companies')
    form_rules = ('tag', )
    form_edit_rules = ('tag',)


class ContactModelView(EnhancedModelView):
    column_list = ('firstname', 'lastname', 'emails',
                   'telephones', 'short_description', *EnhancedModelView.columns_list_extra)
    column_searchable_list = ('firstname', 'lastname',)
    column_sortable_list = ('firstname', 'lastname')
    column_details_list = (
        'firstname', 'lastname', 'description', 'images', 'bio', 'belief_statement',
        'addresses',
        'emails', 'telephones', 'companies', 'message_channels', 'subgroups', 'tf_app', 'tf_web', 'referral_code',
        'deals', 'events', 'comments', 'tasks', 'projects', 'messages', 'sprints', 'links', 'owner', 'ownerbackup', 'author_last', 'author_original', 'updated_at')

    column_filters = ('id', 'firstname', 'lastname', 'description', 'emails', 'telephones', 'addresses.country', 'message_channels', 'referral_code',
                      'deals', 'comments', 'tasks', 'projects', 'companies', 'messages', 'sprints', 'links', 'owner', 'events',
                      'ownerbackup')

    form_rules = (
        'firstname', 'lastname', 'images', 'description', 'bio', 'belief_statement',
        'addresses', 'emails', 'telephones', 'companies', 'message_channels', 'subgroups', 'tf_app', 'tf_web', 'referral_code',
        'deals', 'comments', 'tasks', 'projects', 'messages', 'sprints', 'links', 'owner', 'ownerbackup')

    form_edit_rules = (
        'firstname', 'lastname', 'images', 'description', 'bio', 'belief_statement',
        'addresses',
        'emails', 'telephones', 'companies', 'tasks', 'deals', 'messages',
        'comments', 'links', 'events',
        'message_channels', 'subgroups', 'tf_app', 'tf_web', 'referral_code', 'owner', 'ownerbackup')

    inline_models = [
        InlineImageModelForm(),
        (AddressModel, {'form_columns': [
            'id', 'street_name', 'street_number', 'zip_code', 'country', 'city', 'state']}),
        InlineEventModelForm(),
        (TaskModel, {'form_columns': [
            'id', 'title', 'description', 'type', 'priority', 'assignee', 'eta', 'deadline']}),
        (MessageModel, {'form_columns': [
            'id', 'title', 'content', 'channel']}),
        (DealModel, {'form_columns': [
            'id', 'name', 'amount', 'currency', 'deal_type', 'description']}),
        (CommentModel, {'form_columns': ['id', 'content']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}), ]

    form_args = {
        'ownerbackup': {'label': 'Backup Owner'},
    }

    mainfilter = "Contacts / Id"


class CompanyModelView(EnhancedModelView):

    column_list = ('name', 'short_description', 'vatnumber',
                   'website', *EnhancedModelView.columns_list_extra)
    column_searchable_list = (
        'id', 'name', 'description', 'vatnumber', 'website',)
    column_sortable_list = ('name',)

    column_details_list = (
        'name', 'description', 'emails', 'telephones',  'addresses', 'vatnumber', 'website', 'tags',
        'deals', 'contacts', 'messages',  'tasks', 'comments', 'links', 'owner', 'ownerbackup', 'author_last', 'author_original', 'updated_at')

    column_filters = (
        'name', 'description', 'emails', 'telephones', 'vatnumber', 'website',
        'deals', 'contacts', 'messages', 'tasks', 'links', 'comments', 'owner', 'ownerbackup',)

    form_rules = (
        'name', 'description', 'emails', 'telephones', 'addresses', 'vatnumber', 'website', 'tags',
        'deals', 'contacts', 'messages', 'tasks', 'links', 'comments', 'owner', 'ownerbackup')

    form_edit_rules = (
        'name', 'description', 'emails', 'telephones', 'addresses', 'vatnumber', 'website', 'tags', 'contacts', 'messages', 'tasks', 'deals',
        'comments', 'links', 'owner', 'ownerbackup')

    inline_models = [
        (AddressModel, {'form_columns': [
            'id', 'street_name', 'street_number', 'zip_code', 'country', 'city', 'state']}),
        (TaskModel, {'form_columns': [
            'id', 'title', 'description', 'type', 'priority', 'assignee', 'eta', 'deadline']}),
        (MessageModel, {'form_columns': [
            'id', 'title', 'content', 'channel']}),
        (DealModel, {'form_columns': [
            'id', 'name', 'amount', 'currency', 'deal_type', 'description', ]}),
        (CommentModel, {'form_columns': ['id', 'content']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}), ]
    form_args = {
        'vatnumber': {'label': 'VAT Number'},

    }
    mainfilter = "Companies / Id"


class OrganizationModelView(EnhancedModelView):

    column_list = ('name', 'emails', 'short_description',
                   'owner', *EnhancedModelView.columns_list_extra)
    column_searchable_list = ('id', 'name', 'description',)
    column_sortable_list = ('name',)
    column_details_list = ('name', 'description', 'emails', 'owner',
                           'tasks', 'users', 'comments', 'messages',
                           'links', 'author_last', 'author_original', 'updated_at')

    column_filters = ('name', 'description', 'emails', 'owner',
                      'tasks', 'users', 'comments', 'messages',
                      'links',)

    form_rules = ('name', 'description', 'emails', 'owner', 'users')

    form_edit_rules = ('name', 'description', 'emails', 'users',
                       'owner', 'tasks', 'links', 'messages', 'comments')

    inline_models = [
        (TaskModel, {'form_columns': [
            'id', 'title', 'type', 'priority', 'assignee', 'eta', 'deadline']}),
        (MessageModel, {'form_columns': ['id', 'title', 'content', 'channel']},
         (CommentModel, {'form_columns': ['id', 'content']})),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}),
    ]
    mainfilter = "Organizations / Id"


class DealModelView(EnhancedModelView):

    column_list = ('name', 'amount', 'currency',
                   'deal_type', 'deal_state', *EnhancedModelView.columns_list_extra)
    column_searchable_list = (
        'id', 'name', 'amount', 'currency', 'deal_type', 'deal_state',)
    column_sortable_list = ('name', 'amount', 'currency',
                            'deal_type', 'deal_state', 'updated_at')
    column_details_list = ('id', 'name', 'description', 'amount', 'currency', 'deal_type', 'deal_state', 'shipping_address', 'is_paid',
                           'contact', 'referrer1', 'referrer2', 'company', 'closed_at', 'referral_code', 'tasks', 'messages', 'links', 'comments', 'author_last', 'author_original', 'updated_at')
    column_filters = ('id', 'name', 'amount', 'currency', 'deal_type', 'deal_state', 'closed_at', 'is_paid', 'referral_code', 'updated_at',
                      'contact', 'company', 'tasks', 'messages', 'comments', )

    form_rules = ('name', 'amount', 'currency', 'deal_type', 'deal_state', 'shipping_address',
                  'contact', 'referrer1', 'referrer2', 'company', 'referral_code', 'comments')

    form_edit_rules = ('name', 'description', 'amount', 'currency', 'deal_type', 'deal_state', 'shipping_address',
                       'contact', 'referrer1', 'referrer2', 'company', 'tasks', 'messages', 'links', 'comments', 'is_paid', 'closed_at', 'referral_code')

    inline_models = [
        (TaskModel, {'form_columns': [
            'id', 'title', 'type', 'priority', 'assignee', 'eta', 'deadline']}),
        (AddressModel, {'form_columns': [
            'id', 'street_name', 'street_number', 'zip_code', 'country', 'city', 'state']}),
        (MessageModel, {'form_columns': ['id', 'title', 'content']}),
        (CommentModel, {'form_columns': ['id', 'content']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}),
    ]
    mainfilter = "Deals / Id"


class ProjectModelView(EnhancedModelView):

    column_list = ('name', 'short_description', 'start_date',
                   'deadline', *EnhancedModelView.columns_list_extra)
    column_searchable_list = (
        'id', 'name', 'description', 'start_date', 'deadline')
    column_sortable_list = ('name', 'start_date', 'deadline')
    column_details_list = ('name', 'description', 'start_date', 'deadline',
                           'promoter', 'sprints', 'tasks', 'messages', 'links', 'guardian', 'author_last', 'author_original', 'updated_at')
    column_filters = ('name', 'description', 'start_date', 'deadline', 'contacts',
                      'promoter', 'sprints', 'tasks', 'messages', 'guardian',)

    form_rules = ('name', 'description', 'start_date', 'deadline',
                  'promoter', 'sprints', 'tasks', 'guardian',)

    form_edit_rules = ('name', 'description',
                       'start_date', 'deadline',
                       'promoter', 'guardian',
                       'tasks', 'messages', 'comments', 'links')

    inline_models = [
        (TaskModel, {'form_columns': [
            'id', 'title', 'type', 'priority', 'assignee', 'eta', 'deadline']}),
        (MessageModel, {'form_columns': ['id', 'title', 'content']}),
        (CommentModel, {'form_columns': ['id', 'content']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}),
    ]
    mainfilter = "Projects / Id"


class SprintModelView(EnhancedModelView):
    column_list = ('name', 'short_description', 'start_date',
                   'deadline', *EnhancedModelView.columns_list_extra)
    column_searchable_list = (
        'id', 'name', 'description', 'start_date', 'deadline')
    column_sortable_list = ('name', 'start_date', 'deadline')
    column_details_list = ('id', 'name', 'description', 'start_date', 'deadline',
                           'project', 'contacts', 'tasks',
                           'comments', 'links', 'messages', 'author_last', 'author_original', 'updated_at')
    column_filters = ('id', 'name', 'description', 'start_date', 'deadline',
                      'project', 'contacts',
                      'comments', 'links', 'messages',)
    form_rules = ('name', 'description', 'start_date', 'deadline',
                  'project',
                  )

    form_edit_rules = ('name', 'description', 'start_date', 'deadline',
                       'project', 'contacts', 'tasks', 'messages', 'comments', 'links')

    inline_models = [
        (TaskModel, {'form_columns': [
            'id', 'title', 'type', 'priority', 'assignee', 'eta', 'deadline']}),
        (MessageModel, {'form_columns': [
            'id', 'title', 'content', 'channel']}),
        (CommentModel, {'form_columns': ['id', 'content']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}),
    ]

    mainfilter = "Sprints / Id"


class CommentModelView(EnhancedModelView):
    column_list = ('id', 'short_content', *
                   EnhancedModelView.columns_list_extra)
    column_searchable_list = ('id', 'content')
    column_sortable_list = ('content',)

    column_details_list = ('id', 'content',
                           'company', 'contact', 'user', 'organization', 'project', 'sprint', 'task',
                           'link', 'deal', 'author_last', 'author_original', 'updated_at')
    column_filters = ('id', 'content',
                      'company', 'contact', 'user', 'organization', 'project', 'sprint', 'task', 'event',
                      'link', 'deal', )
    form_rules = ('content', 'user',
                  'company', 'contact', 'organization', 'project', 'sprint', 'task',
                  'link', 'deal',)
    form_edit_rules = ('content',)


class LinkModelView(EnhancedModelView):
    column_list = ('url', 'labels', *EnhancedModelView.columns_list_extra)
    column_searchable_list = ('id', 'url', 'labels')
    column_sortable_list = ('url',)
    column_details_list = ('url', 'contact', 'user', 'company', 'organization', 'task', 'project',
                           'deal', 'sprint', 'labels', 'comments', 'author_last', 'author_original', 'updated_at')

    column_filters = ('url', 'contact', 'user', 'company', 'organization', 'task', 'project',
                      'deal', 'sprint', 'labels', 'comments', 'event')

    form_rules = ('url', 'user', 'contact', 'company', 'organization', 'task', 'project',
                  'deal', 'sprint', 'labels',)
    form_edit_rules = ('url', 'labels')

    mainfilter = 'Links / Id'


class TaskModelView(EnhancedModelView):
    column_list = ('title', 'type', 'priority', 'state', 'assignee', 'user', 'contact',
                   'organization', 'company', 'project', 'sprint', 'deal', *EnhancedModelView.columns_list_extra)
    column_searchable_list = ('id', 'title', 'description',
                              'type', 'priority', 'assignee.firstname', 'assignee.lastname', 'assignee.username')
    column_sortable_list = (['priority', 'updated_at'])
    column_details_list = ('id', 'title', 'description', 'type', 'priority', 'eta', 'deadline', 'state',
                           'time_done', 'time_estimate', 'assignee', 'user', 'contact',
                           'company', 'organization', 'project', 'sprint', 'deal',
                           'comments', 'messages', 'links', 'author_last', 'author_original', 'updated_at')

    column_filters = ('id', 'title', 'description', 'type', 'priority', 'eta', 'deadline', 'time_done',
                      'contact', 'user', 'assignee.username', 'assignee.id', 'assignee.firstname', 'assignee.lastname',
                      'company', 'organization', 'project', 'sprint', 'deal',
                      'comments', 'messages')
    form_rules = ('title', 'description',
                  'type', 'priority', 'eta', 'deadline', 'assignee',
                  'user', 'contact', 'company', 'organization', 'project', 'sprint', 'deal')

    form_edit_rules = ('title', 'description', 'eta', 'deadline', 'assignee', 'user', 'contact', 'state',
                       'type', 'priority', 'time_done', 'comments', 'messages', 'links')

    inline_models = [
        (CommentModel, {'form_columns': [
            'id', 'content', ]}),
        (MessageModel, {'form_columns': [
            'id', 'title', 'content', 'channel']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}),
    ]


class MessageModelView(EnhancedModelView):
    column_list = ('author', 'title', 'short_content',
                   'company', 'contact', 'deal', 'organizaton', 'task', 'project', 'sprint', 'author', 'time_tosend', 'time_sent', *EnhancedModelView.columns_list_extra)
    column_searchable_list = ('title', 'content')
    column_sortable_list = ('title', 'author')

    column_details_list = ('id', 'title', 'destination', 'author', 'content', 'company',
                           'contact', 'organization', 'project', 'sprint', 'deal', 'task', 'time_tosend', 'time_sent',
                           'author_last', 'author_original', 'updated_at')

    form_rules = column_filters = ('title', 'content', 'channel', 'time_tosend', 'time_sent',
                                   'company', 'contact', 'author', 'organization', 'project', 'sprint', 'deal', 'task', 'event')

    form_edit_rules = ('title', 'author', 'content', 'channel',
                       'time_tosend', 'time_sent',)


class TaskAssignmentModelView(EnhancedModelView):
    column_list = ('percent_completed', 'contact',
                   'task', *EnhancedModelView.columns_list_extra)
    column_details_list = ('contact', 'task', 'tasktracking')


class TaskTrackingModelView(EnhancedModelView):
    column_list = column_details_list = ('remarks',
                                         'time_done', *EnhancedModelView.columns_list_extra)


class EventModelView(EnhancedModelView):
    column_list = ('title', 'description',
                   'event_datetime',  *EnhancedModelView.columns_list_extra)
    column_searchable_list = ('title', 'event_datetime')
    column_sortable_list = ('title', 'event_datetime')

    column_details_list = ('id', 'title', 'description', 'event_datetime',
                           'contacts', 'messages', 'comments', 'links',
                           'author_last', 'author_original', 'updated_at')

    column_filters = ('id', 'title', 'description',
                      'event_datetime', 'contacts')

    form_rules = ('title', 'description',
                  'event_datetime', 'contacts', 'links')

    form_edit_rules = ('title', 'description',
                       'event_datetime', 'contacts', 'messages', 'comments', 'links')

    inline_models = [
        (MessageModel, {'form_columns': [
            'id', 'title', 'content', 'channel']}),
        (CommentModel, {'form_columns': ['id', 'content']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}),
    ]

    mainfilter = "Events / Id"

# class AlertModelView(EnhancedModelView):
#     pass
#
# class AlertSourceModelView(EnhancedModelView):
#     pass
#
# class AlertProfileModelView(EnhancedModelView):
#     pass
#


class KnowledgeBaseModelView(EnhancedModelView):
    pass
#


class KnowledgeBaseCategoryModelView(EnhancedModelView):
    pass
