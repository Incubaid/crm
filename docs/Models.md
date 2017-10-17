## Models

To define a model follow the following conventions

- Every subpackage under ```crm``` represents a sub application i.e ```contact```
- By default if you want to add a model a sub application, add them in a file called ```models.py```; i.e ```crm./contact/models.py```
- model files ```models.py``` along all sub applications are registered automatically
- Each model Object **(That is not many to many )** inherit from ```(crm.db.Model & crm.db.BaseModel)```

- Each **(Many To Many)** model inherits from ```(crm.db.Model & crm.db.ManyToManyBaseModel)```
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

- Root models are basically basic (main) models in our CRM system and they can contain other non main models and we export them only
and include non main models data in them; i.e ```User```
an examle of non main model is a ```Task``` since ```User can hold tasks```
    - we have 6 Root models
        - Company
        - Contact
        - Deal
        - Sprint
        - Project
        - Organization
        - User
    - To make a model, a main model, you need to inherit from  ```(crm.db.MainModel)```
    - Exmaple:
        ```python
                from crm.db import db, BaseModel, RootModel


                class Company(db.Model, BaseModel, RootModel):

                    __tablename__ = "companies"

                    name = db.Column(
                        db.String(255),
                        nullable=False
                    )

                    # should be markdown.
                    description = db.Column(
                        db.Text()
                    )
        ```


#### WHy the hell did we differentiate between normal models and many2many models

- Many2Many models cause problems if they use the same ID generation mechanism
we are using i.e ```random 5 chars ID``` in flask admin
so we need to keep them using the normal auto incremental integer IDs

- Many2Many fields contain ```IS_MANY_TO_MANY``` property to differentiate them

- Many2Many fields are separate objects (non-roots) that need to have special treatment during ```loaddata``` & ```dumpdata```
