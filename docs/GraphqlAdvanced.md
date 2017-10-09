## Defining Types, Queries, Mutations

- All graphql URLs/end points are exposed through the sub application ```crm.api```, in ```crm.api.views```
- We have 2 main end points
    - ```/graphql``` web based console to test graphql
    - ```/api``` can be called using any HTTP client

### Defining Types, Queries and Mutations

- [Graphql](http://graphql.org/learn/) APIs are exposed in module called ```graphql.py``` that
lives inside your sub appliction i.e ```crm.contact.graphql.py```
If your sub application contains this module, it will be loaded automatically and your API will
get public instantly

- There's another module called ```crm.graphql``` this only defines common types that
your API definitions must use.
Don't touch that file

- In order to expose a [Graphql](http://graphql.org/learn/) API to a model in a sub application
you need to do the following
    - create ```graphql.py``` module in your sub application
    - Expose a [Graphene](http://docs.graphene-python.org) SQLALCHEMY type our of your model. This will be used by your queries and mutations
        - A type is what is returned in results and you can add extra fields to a [Graphene](http://docs.graphene-python.org) SQLALCHEMY type
         that was not originally in your models
    - define your queries in a class that inherits from ```crm.graphql.BaseQuery```
    - define your mutations in a class that inherits from ```crm.graphql.BaseMutation```


#### Types definitions
- Use the following example, just replace your model with the actual model in your sub application and change the class name of course
    ```python
    class ContactType(SQLAlchemyObjectType):
        uid = graphene.String()

        class Meta:
            model = Contact # only change this
            interfaces = (relay.Node,)
            name = model.__name__
    ```

- we add a ```(uid)``` field here because [Graphene](http://docs.graphene-python.org) replaces our records ID with internal representation
of that ID. so we add an extra ```(uid)``` field that contains the actual value of the ```(id)``` field
- we then automatically manipulate all records coming from a query and fill that ```uid``` field with the original
value of ```object.id```


**Query definitions**
- Use the following example, rename necessary fields
    ```python
    class ContactQuery(BaseQuery):
        """
        we have 2 queries here contact and contacts
        """

        contacts = CRMConnectionField(ContactType)
        # contact query to return one contact and takes (uid) argument
        # uid is the original object.id in db
        contact = graphene.Field(ContactType, uid=graphene.String())

        def resolve_contact(self, context, uid):
            return ContactType.get_query(context).filter_by(id=uid).first()

        class Meta:
            interfaces = (relay.Node,)
    ```
- In previous example we define 2 queries:
    - ```contacts``` returning all /subset of records.
    - ```contact``` takes ```uid``` field and returns one record
- For each query you define, usually you define the ```query_name```and a resolver function
```resolve_{query_name}``` that is used when query executed
- Sometimes a resolver function may not be needed for queries of type ```CRMConnectionField```
    - these queries return all/subset of data automatically from your model
    - i.e ```contacts``` query, however we may need to add a resolver function later to contacts if we need
    add more filtration options

**Mutations definitions**
- Define your mutations in classes that extend ```graphene.Mutation```
    - ```class CreateContact(graphene.Mutation):pass```
    - ```class UpdateContact(graphene.Mutation):pass```
- Define your Mutation class that holds all these related mutations in one place in a class that extends ```crm.graphql.BaseMutation```
    -
    ```python
    class ContactMutation(BaseMutation):
    """
    Put all contact mutations here
    """
        create_contact = CreateContact.Field()
        update_contact = UpdateContact.Field()
    ```

- What is the structure of your mutation classes like ```CreateContact```?
    - You define fields in that class that will be returned when mutation is executed
        - we return 3 fields:
            - actual object
            - ok (boolean means success or failure)
            - errors conatins errors (if any)
    - You define inner class called Arguments containing the mutation arguments
    - you override ```mutate(cls, root, context, **kwargs)``` function which contains logic to handle the
    mutation

    - Example:

        ```python
        class CreateContact(graphene.Mutation):
            class Arguments:
                """
                    Mutation Arguments
                """
                firstname = graphene.String(required=True)

            # MUTATION RESULTS FIELDS
            contact = graphene.Field(ContactType)
            ok = graphene.Boolean()
            errors = graphene.types.json.JSONString()

            @classmethod
            def mutate(cls, root, context, **kwargs):
                """
                Mutation logic is handled here
                """

                errors = {
                    'fields': {},
                    'code': 400
                }


                form = ContactForm(werkzeug.MultiDict(kwargs), Contact)
                if not form.validate():
                    errors['fields'].update(form.errors)
                    return CreateContact(contact=None, ok=False, errors=errors)

                contact = Contact(**form.data)
                db.session.add(contact)
                db.session.commit()

                return CreateContact(contact=contact, ok=True, errors=None)
        ```

