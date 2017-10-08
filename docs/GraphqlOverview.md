## Graphql Overivew

### Intro about Graphql with Flask
- We depend on a library called [Graphene](http://docs.graphene-python.org)
- To read about graphene with flask [Start here](http://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/#creating-graphql-and-graphiql-views-in-flask)


### CRM Graphql API endpoints

- You can test graphql queries through the UI interface at the end point url ```/graphql```
![graphql interface](assets/graphql_query.png)
- using any HTTP client you als send requests to the end point url ```/api```
- All graphql URLs/end points are exposed through the sub application ```crm.api```, in ```crm.api.views```

### Defining Types, Queries and Mutations

You can define your own Graphql Types, Queries or Mutations in ```graphql.py``` file
inside your sub application i.e ```crm.contact.graphql.py```
This will be recognized automatically and exposed

**Types definitions**
- You define Graphql Types from your model same way done in the following example
    ```python
    from graphene_sqlalchemy import SQLAlchemyObjectType

    from .models import Contact


    class ContactType(SQLAlchemyObjectType):
        class Meta:
            model = Contact
     ```

**Query definitions**
- You define queries on a a graphql type same way in the following example
    ```python
    class ContactQuery(graphene.AbstractType):
        contacts = graphene.List(ContactType)

        def resolve_contacts(self, args, context, info):
            query = ContactType.get_query(context)
            return query.all()
     ```
