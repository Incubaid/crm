## DB Migrations

**What is DB Migrations**

During the life time of a project, you start with a certain db schema
which evolves over time.
Nothing wrong with evolution, yet the problem is how will you migrate
production database into the new schema and how will you update
affected records, delet ones that are no longer needed or change
column names or constraints or types in a way that keeps application
running and doesn't affect existing data
[Read more on this](https://en.wikipedia.org/wiki/Schema_migration)

**How migrations work**
- We use [Flask migrate](https://flask-migrate.readthedocs.io/en/latest/)
- Use these commands if you don't have previously created migration scripts:
    - ```flask createdb``` Create database  *ONLY IF YOUR ARE NOT USING [SQLITE](https://www.sqlite.org/)*
    - ```flask db init``` Create *migrations* directory.
    - ```flask db migrate``` Create initial migration script (revision 1) under *migrations/versions* dir
    - ```flask db upgrade``` Create tables physically in DB
- Do the following if you have changes in DB that you want to migrate to
    - ```flask db migrate``` will compare models in your app with the migration scripts in the *migrations/versions* dir
    then create a new version that can be used to migrate DB from current state to the new state as models
    - ```flask db upgrade``` Update DB up to latest revision

- Flask migrations uses a library called [Alembic](http://alembic.zzzcomputing.com/en/latest/tutorial.html)
Consider reading the documentation there especially if you want to alter data in database during migrations

### WARNINGS

- Flask migration framework not being able to detect changes
in SQLALCHEMY ```Enum``` types so it's automatically created for you
you have to make sure whenever you change an ```Enum``` type that you make the migration
manually.
An example below on how to deal with this situation

- In case of sqlite, you can use ```flask db init flask db migrate flask db upgrade``` and database
will be created for you.
but in case of other RDBMS like postgres or mysql, you need to create DB first using ```flask createdb```


### Full Migrations Scenario**

Now we're in production and we've live data out there!
Our ```producction``` branch contains a directory called migrations
contining all old migrations files used through the life time of our application.
Now we have changs in ```master``` branch in models
what to do to create mogrations files to migrate production db

Our ```master``` branch doesn't contain ```migrations``` DIR persistent in git
i.e it's added to ```.gitignore``` so it's not committed there


- Switch your app to use ```postgres`` DB
- commit all your changes into ```master``` branch
- delete ```migrations``` DIR if there
- switch to ```production``` branch
- drop the used Database
    - in postgresql console use ```DROP DATABASE my-db;```

- Run ```flask db upgrade``` to initiate the DB wit old/production state
- If you have data from production in ```DATA``` DIR RUN ```flask loaddata```
- Copy ```production``` branch ```migrations``` DIR to any temporary location
- Swittch to ```master``` branch
- copy migrations DIR, from your temporary location into crm/migrations
- Now you need to run ```flask db migrate``` this will create a new revision/migration file
that can move DB from old state to new state.
We have used ```migrations``` dir, so we now sure that we used all previous migrations
and we created a new one that depends on them
- Edit your newly migration file under ```migrations/revisions``` if needed
- commit in ```production``` after merging ```master``` into priduction
- **Check code in [migrations files](https:https://github.com/Incubaid/crm/blob/production/migrations/versions/88bd97fd024f_.py) to see how you can query and alter data during migrations

### Deal with Enum changes**
We had this issue once before
- Old ENum
    ```python
    class DealCurrency(Enum):
        USD, EUR, AED, GBP = range(4)
    ```

- New Enum
    ```python
    class DealCurrency(Enum):
        USD, EUR, AED, GBP, BTC = range(5)
    ```

- Now after creating new migration file, these changes was not detected
- How to do the migrarion?
    - since old and new enum names are same, and you can't just create enum with same name as old one
       We create temporary type with different enum name but holding new data

    - we alter table field to use the temp one, then we drop old one
    - we create new one and alter table field with to use the new then we drop temp one

        ```
        ## Deal Currency
        old_dealcurrency = postgresql.ENUM('USD', 'EUR', 'AED', 'GBP' , name='dealcurrency')
        new_dealcurrency = postgresql.ENUM('USD', 'EUR', 'AED', 'GBP', 'BTC' , name='dealcurrency')
        temp_dealcurrency = postgresql.ENUM('USD', 'EUR', 'AED', 'GBP', 'BTC' , name='_dealcurrency')

        def update_deal_enums():
            temp_dealcurrency.create(op.get_bind(), checkfirst=False)
            op.execute('ALTER TABLE deals ALTER COLUMN currency TYPE _dealcurrency'
                       ' USING currency::text::_dealcurrency')

            old_dealcurrency.drop(op.get_bind(), checkfirst=False)
            # Create and convert to the "new" status type
            new_dealcurrency.create(op.get_bind(), checkfirst=False)

            op.execute('ALTER TABLE deals ALTER COLUMN currency TYPE dealcurrency'
                       ' USING currency::text::dealcurrency')

            temp_dealcurrency.drop(op.get_bind(), checkfirst=False)


        def upgrade():
            ...
            ...
            update_deal_enums()
        ```
