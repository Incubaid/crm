from graphene_django import DjangoObjectType
import graphene

from .forms import ContactPhoneForm, ContactEmailForm, ContactForm
from .models import Contact, ContactEmail, ContactPhone
from graphene_django.filter import DjangoFilterConnectionField

from django.db import transaction

from django.core import serializers
from .signals import contact_added, contact_updated, contact_deleted


class ContactNode(DjangoObjectType):
    class Meta:
        model = Contact
        name = "contact"
        filter_fields = {
            'last_name': ['exact', 'iexact', 'icontains'],
            'first_name': ['exact', 'iexact', 'icontains'],
            'description': ['exact', 'iexact', 'icontains'],
            'telegram': ['iexact', 'icontains'],
            'owner__first_name': ['exact', 'iexact', 'icontains'],
            'owner__last_name': ['exact', 'iexact', 'icontains'],
            'owner_backup__first_name': ['exact', 'iexact', 'icontains'],
            'owner_backup__last_name': ['exact', 'iexact', 'icontains'],
            'emails__email': ['exact', 'icontains'],
            'phone_numbers__phone': ['iexact', 'icontains'],
            'created_at': ['exact', 'range']
        }

        interfaces = (graphene.relay.Node,)


class ContactQuery(graphene.ObjectType):
    contacts = DjangoFilterConnectionField(ContactNode)
    contact = graphene.Field(ContactNode, pk=graphene.String())

    def resolve_contact(self, info, pk):
        return Contact.objects.get(pk=pk)


class CreateContact(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        description = graphene.String()
        is_user = graphene.Boolean()
        telegram = graphene.String()
        emails = graphene.List(graphene.String)
        phones = graphene.List(graphene.String)

    contact = graphene.Field(ContactNode)
    ok = graphene.Boolean()
    errors = graphene.JSONString()

    @classmethod
    @transaction.atomic
    def mutate(cls, root, context, **kwargs):
        emails = [ContactEmail(email=email) for email in kwargs.get('emails', [])]
        phones = [ContactPhone(phone=phone) for phone in kwargs.get('phones', [])]

        errors = {
            'fields': {},
            'code': 400
        }

        OK = True
        contact_form = ContactForm(kwargs)
        if not contact_form.is_valid():
            OK = False
            errors['fields'].update(contact_form.errors)

        for phone in phones:
            form = ContactPhoneForm({'phone':phone.phone})
            if not form.is_valid():
                OK = False
                errors['fields']['phones'] = errors['fields'].get('phones', [])
                errors['fields']['phones'].append(form.errors.values()[0])
        for email in emails:
            form = ContactEmailForm({'email':email.email})
            if not form.is_valid():
                OK = False
                errors['fields']['emails'] = errors['fields'].get('emails', [])
                errors['fields']['emails'].append(form.errors.values()[0])

        if not OK:
            return CreateContact(contact=None, ok=False, errors=errors)

        contact = contact_form.save()

        for phone in phones:
            phone.contact = contact
            phone.save()

        for email in emails:
            email.contact = contact
            email.save()

        models = [contact] + phones + emails

        contact_added.send(
            sender=cls,
            request=context.context,
            data={'add': serializers.serialize('json', models)}
        )
        return CreateContact(contact=contact, ok=True, errors=None)


class UpdateContact(graphene.Mutation):
    class Arguments:
        pk = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        description = graphene.String()
        is_user = graphene.Boolean()
        telegram = graphene.String()
        emails = graphene.List(graphene.String)
        phones = graphene.List(graphene.String)

    contact = graphene.Field(ContactNode)
    ok = graphene.Boolean()
    errors = graphene.JSONString()

    @classmethod
    @transaction.atomic
    def mutate(cls, root, context, **kwargs):
        pk = kwargs.get('pk')
        emails = [ContactEmail(email=email) for email in kwargs.get('emails', [])]
        phones = [ContactPhone(phone=phone) for phone in kwargs.get('phones', [])]

        errors = {
            'fields': {},
            'code': 400
        }

        try:
            instance = Contact.objects.get(pk=pk)
        except Contact.DowsNotExist:
            errors['code'] = 404
            return CreateContact(contact=None, ok=False, errors=errors)

        contact_form = ContactForm(data=kwargs, instance=instance)
        OK = True
        if not contact_form.is_valid():
            OK = False
            errors['fields'].update(contact_form.errors)

        for phone in phones:
            form = ContactPhoneForm({'phone':phone.phone})
            if not form.is_valid():
                OK = False
                errors['fields']['phones'] = errors['fields'].get('phones', [])
                errors['fields']['phones'].append(form.errors.values()[0])
        for email in emails:
            form = ContactEmailForm({'email':email.email})
            if not form.is_valid():
                errors['fields']['emails'] = errors['fields'].get('emails', [])
                errors['fields']['emails'].append(form.errors.values()[0])

        if not OK:
            return CreateContact(contact=None, ok=False, errors=errors)

        contact = contact_form.save()

        data = {
            'update': serializers.serialize('json', [contact]),
            'delete':[],
            'add': []
        }

        if phones:
            phones = contact.phone_numbers.all()
            data['delete'].extend( serializers.serialize('json', phones))
            phones.delete()

        if emails:
            emails = contact.emails.all()
            data['delete'].extend(serializers.serialize('json', emails))
            emails.delete()

        for phone in phones:
            phone.contact = contact
            data['add'].extend(serializers.serialize('json', [phone]))
            phone.save()

        for email in emails:
            email.contact = contact
            data['add'].extend(serializers.serialize('json', [email]))
            email.save()

        contact_updated.send(
            sender=cls,
            request=context.context,
            data=data
        )

        return CreateContact(contact=contact, ok=True, errors=None)


class DeleteContact(graphene.Mutation):
    class Arguments:
        pk = graphene.String(required=True)

    contact = graphene.Field(ContactNode)
    ok = graphene.Boolean()
    errors = graphene.JSONString()

    @classmethod
    @transaction.atomic
    def mutate(cls, root, context, **kwargs):

        errors = {
            'fields': {},
            'code': 404
        }

        try:
            instance = Contact.objects.get(pk=kwargs.get('pk'))
            models = [instance] + [phone for phone in instance.phone_numbers.all()] + [email for email in instance.emails.all()]
            instance.delete()

            contact_deleted.send(
                sender=cls,
                request=context.context,
                data = {'delete': serializers.serialize('json', models)}
        )

            return CreateContact(contact=instance, ok=True, errors=None)
        except Contact.DoesNotExist:
            errors['code'] = 404
            return CreateContact(contact=None, ok=False, errors=errors)


class ContactMutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
    update_contact = UpdateContact.Field()
    delete_contact = DeleteContact.Field()
