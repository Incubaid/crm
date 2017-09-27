## Models

To define a model follow the following conventions

- Every subpackage under ```crm``` represents a sub application i.e ```contact```
- By default if you want to add a model a sub application, add them in a file called ```models.py```; i.e ```crm./contact/models.py```
- model files ```models.py``` along all sub applications are registered automatically
- Each model Object inherit from ```(crm.db.db & crm.db.BaseModel)```
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

