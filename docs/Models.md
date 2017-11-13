## Models

- All models **Must** be defined under `crm.apps.{my_sub_app}.models` an example is `crm.apps.user.models`
- ِAll models inherit from `db.Model`

> There's difference between (Many To Many) models and non (Many To Many) models
And we need a way to differentiate between both especially when we export/import DB data
So each category has different Parent class.That says `flask dumpdata` & `flask loaddata` commands
will not work correctly if you're not inheriting from proper parent while defining your model

- **Many To Many**

    - Must inherit from `crm.db.ManyToManyBaseModel)`
    - Primary Key (id) field is integer and auto incremental
    - Usually records in these tables are auto created by Flask ORM [SqlAlchemy](https://www.sqlalchemy.org/)
      That's why we don't want to alter their creation mechanism.

     ```python
        class ContactSubgroup(db.Model, ManyToManyBaseModel):
            __tablename__ = "contacts_subgroups"

            subgroup_id = db.Column(
                db.String(5),
                db.ForeignKey('subgroups.id')
            )

            contact_id = db.Column(
                db.String(5),
                db.ForeignKey("contacts.id")
            )
     ```


- **(Non Many to Many)**

    - Must inherit from `crm.db.BaseModel`
    - Primary Key (id) is string of unique 5 characters and assigned by an ORM [SqlAlchemy Event](http://docs.sqlalchemy.org/en/latest/orm/events.html)
        > `crm.events.update_auto_fields` registers a `before_flush` event to update id field with a unique ID string
           This event finds newly created records and alter their IDS with random ones.

        > Note that newly created tables list in a DB `session.new` doesn't contain any many to many field
           so we're sure that only non Many to Many fields are affected

    ```
    class Contact(db.Model, BaseModel, RootModel):

    __tablename__ = "contacts"

    firstname = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    lastname = db.Column(
        db.String(255),
        default="",
        index=True
    )
    description = db.Column(
        db.Text()
    )
    ```


- **Root models**
    > We've 7 Root models,
        - Company
        - Contact
        - Deal
        - Sprint
        - Project
        - Organization
        - User

    - Root models are these that is exported during `flask dumpdata` command
    - A Root model must inherit from `crm.db.RootModel`
    - Since only Root models are exported during `flask dumpdata`, all info related to a record from any other non Root
    model is contained inside Root model data, that says exported data has duplications but more readable
