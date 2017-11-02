### Load & Dump Data into/From JSON Algorithms
- `flask dumpdata` dumps DB data into JSON
- `flask loaddata` loads data from JSON
- `flask dumpcache` dumps cached changes into the proper JSON file(s)

**Dump**

 >  `flask dumpdata`

- Only Root models are dumped, A DIR with the model class name is created

    > We've 7 Root models/DIRs
            - Company
            - Contact
            - Deal
            - Sprint
            - Project
            - Organization
            - User
- In each Dir, all records in a Root model are dumped into files, where each file represents one record.
Each file name starts with the `id` of the object

- Dumped data **must be Sorted** so if these data is saved into a [Git](https://git-scm.com/) repo, only there's a change
in Data if it's actually changed.

- Each model object has `as_dict` method, that returns object as dict and we can dump it into JSON

- We use [ujosn](https://pypi.python.org/pypi/ujson) for fast dump of data. but with only one problem that it
dumps datetime fields into epoch so you'll have to reverse epoch into datetime when loading object from JSON

- `obj.as_dict()` does the following:
    - create an empty dict
    - Add key `model` and value is the Model name
    - Loop over all fields in an object.
        - If field is string/numeric or datetime add it to dict directly
        - If field is enum, add field name as key and value to be `enum_field.name`
        - If field is a backref relation i.e `contact.tasks`, then we add field name as key and value to be list
        and for each object in the backref relation we call `obj.as_dict()` but we don't resolve these objects backref relations
        otherwise we'll end up in recursion error and we only care about actual objects not their backref relations
        - For each backref relation you find, if it refers to many to many table, add it to alist for further processing later
        - If field is Foreign Key add field name as key and value to be Foreign `object.as_dict()` and again we don't care about the backref relations of foreign key object

        - for each many to many relationship in a model object
            - add key with the table name and value of a list of dicts from many2any field thaictt belongs to the current object
