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

**WARNING**

In case of sqlite, you can use ```flask db init flask db migrate flask db upgrade``` and database
will be created for you.
but in case of other RDBMS like postgres or mysql, you need to create DB first
