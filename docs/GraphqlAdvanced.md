## Defining Types, Queries, Mutations

- All graphql URLs/end points are exposed through the sub application ```crm.api```, in ```crm.api.views```
- We have 2 main end points
    - ```/graphql``` web based console to test graphql
    - ```/api``` can be called using any HTTP client

### Defining Types, Queries and Mutations

- For any sub application i.e `crm.apps.contact`, you can define [Graphql](http://graphql.org/learn/) APIs
in a package called `crm.apps.{app_name}.graphql` and your queries and mutations will be exposed automatically

- Each  `crm.apps.{app_name}.graphql` package must contain 3 modules:
    - `types.py`
        - where you define `graphql` types from certain [SqlAlchemy](https://www.sqlalchemy.org/) model in the
          same manner you define [Django model forms](https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/)
    - `arguments.py`
        - These are the arguments for mutations and queries and they're simply defined by defining some/all fields
        from certain model
    - `mutations.py`
        - Where you define your mutations
    - `queries.py`
        - Where you define queries


#### Types definitions
- Add your type in `crm.apps.{app_name}.graphql.types` module
    - Inherit from ```SQLAlchemyObjectType```
    - In your Meta class, define ```model = your-model```
    - Add extra fields if needed


    ```python
    import graphene
    from graphene import relay
    from graphene_sqlalchemy import SQLAlchemyObjectType

    from crm.apps.contact.models import Contact

    class ContactType(SQLAlchemyObjectType):
        uid = graphene.String()

        class Meta:
            model = Contact
            interfaces = (relay.Node,)
            name = model.__name__
    ```

**Important**
[Graphene](http://docs.graphene-python.org) replaces record `id` with internal representation of that `id`
so we use `uid` in all our [Graphene](http://docs.graphene-python.org) types to represent original `id`
that is why it's important to add `uid = graphene.String()` in each type you define which will be mapped automatically
to `object.uid` which returns `object.id` value

#### Arguments definitions
- Add your arguments in `crm.apps.{app_name}.graphql.arguments` module
- we have usually 3 types of arguments
    - `Base Arguments`
        - Inherits from `graphene.types.inputobjecttype.InputObjectType` & `crm.graphql.BaseArgument`
        - Parent for all arguments, each field in it is defined as (not required)
        - We basically define same fields in a certain model
    - `Create mutation arguments`
        - Inherits from `Base Arguments`.
        - Override required fields by redefining them with `required=True` param
    - `Update mutation arguments`
        - Inherits from `Base Arguments`.
        - Add `uid = graphene.String(required=True)` because while updating a record `uid` is definitely required
- Example: `crm.apps.contact.graphql.arguments`
```python
        import graphene
        from graphene.types.inputobjecttype import InputObjectType

        from crm.apps.address.graphql.arguments import AddressArguments
        from crm.apps.comment.graphql.arguments import CommentArguments
        from crm.apps.contact.models import Gender
        from crm.apps.link.graphql.arguments import LinkArguments
        from crm.apps.message.graphql.arguments import MessageArguments
        from crm.apps.passport.graphql.arguments import PassportArguments
        from crm.apps.task.graphql.arguments import TaskArguments
        from crm.graphql import BaseArgument


        class ContactSubgroupArguments(InputObjectType):
            groupname = graphene.String()


        class ContactArguments(InputObjectType, BaseArgument):
            uid = graphene.String()
            firstname = graphene.String()
            lastname = graphene.String()
            gender = graphene.Enum.from_enum(Gender)()
            description = graphene.String()
            bio = graphene.String()
            belief_statement = graphene.String()
            message_channels = graphene.String()
            owner = graphene.Argument('crm.apps.user.graphql.arguments.UserArguments')
            ownerbackup = graphene.Argument('crm.apps.user.graphql.arguments.UserArguments')
            parent = graphene.Argument('crm.apps.contact.graphql.arguments.ContactArguments')
            emails = graphene.String()
            telephones = graphene.String()
            tf_app = graphene.Boolean()
            tf_web = graphene.Boolean()
            referral_code = graphene.String()

            deals = graphene.List('crm.apps.deal.graphql.arguments.DealArguments')
            comments = graphene.List(CommentArguments)
            tasks = graphene.List(TaskArguments)
            messages = graphene.List(MessageArguments)
            links = graphene.List(LinkArguments)

            subgroups = graphene.List(ContactSubgroupArguments)
            addresses = graphene.List(AddressArguments)
            passports = graphene.List(PassportArguments)


        class CreateContactArguments(ContactArguments):
            firstname = graphene.String(required=True)
            lastname = graphene.String(required=True)


        class UpdateContactArguments(ContactArguments):
            uid = graphene.String(required=True)


```


#### Query definitions
- Add your arguments in `crm.apps.{app_name}.graphql.queries` module
- Inherit from `crm.graphql.BaseQuery`

- Use the following example, rename necessary fields
    ```python
        import graphene
        from graphene import relay

        from crm.apps.contact.graphql.arguments import ContactArguments
        from crm.apps.contact.graphql.types import ContactType
        from crm.graphql import BaseQuery, CRMConnectionField


        class ContactQuery(BaseQuery):
            """
            we have 2 queries here contact and contacts
            """

            # no need for resplve_contacts function here
            contacts = CRMConnectionField(
                ContactType,
                **ContactArguments.fields()

            )
            # contact query to return one contact and takes (uid) argument
            # uid is the original object.id in db
            contact = graphene.Field(ContactType, uid=graphene.String())

            def resolve_contact(self, context, uid):
                return ContactType.get_query(context).filter_by(id=uid).first()


            class Meta:
                interfaces = (relay.Node, )
    ```
- In previous example we define 2 queries:
    - ```contacts```
        - returning all/subset of records. Please refer to [CRM API General overview](GraphqlQueriesAndMutations.md) & [GraphQl API Query language](GraphqlQueryLanguage.md) for examples on how to query data
        - may take no arguments then return all records
        - may take query arguments defined by `ContactArguments` then return subset of data based on the defined query

    - ```contact``` takes ```uid``` field and returns one record
- For each query you define, usually you define the ```query_name``` i.e `contacts` and a resolver function
```resolve_{query_name}``` i.e `resolve_contacts` that is called to handle that query when executed



#### Mutations definitions
- Add your mutations in `crm.apps.{app_name}.graphql.mutations` module
- For each mutation you have, you create a class that extends `graphene.Mutation` and override `mutate` function
and may uses one of the `arguments` defined in `crm.apps.{app_name}.graphql.arguments`

    ```
    class CreateContacts(graphene.Mutation):
        class Arguments:
            """
                Mutation Arguments
            """
            records = graphene.List(CreateContactArguments, required=True)

        ok = graphene.Boolean()
        ids = graphene.List(graphene.String)

        @classmethod
        def mutate(cls, root, context, **kwargs):
            """
            Mutation logic is handled here
            """
            ...

    class UpdateContacts(graphene.Mutation):
        class Arguments:
            """
                Mutation Arguments
            """
            records = graphene.List(UpdateContactArguments, required=True)

        ok = graphene.Boolean()
        ids = graphene.List(graphene.String)

        @classmethod
        def mutate(cls, root, context, **kwargs):
            """
            Mutation logic is handled here
            """
            ...

    class DeleteContacts(graphene.Mutation):
        class Arguments:
            """
                Mutation Arguments
            """
            uids = graphene.List(graphene.String, required=True)

        ok = graphene.Boolean()

        @classmethod
        def mutate(cls, root, context, **kwargs):
            """
            Mutation logic is handled here
            """
            ...
    ```

- Define Mutation parent class that holds all defined mutations and that extends ```crm.graphql.BaseMutation```
    ```python
    class ContactMutation(BaseMutation):
        """
        Put all contact mutations here
        """
        create_contacts = CreateContacts.Field()
        delete_contacts = DeleteContacts.Field()
        update_contacts = UpdateContacts.Field()
    ```