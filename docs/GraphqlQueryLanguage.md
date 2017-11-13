### Query Language
We use our own query language to query Data in CRM
In any query, you define a field name and its value as a query string i.e `contacts({'firstname': 'my-query'}){..}`

#### Query String structure

- Exact match `=`
    - Use string you want to match directly i.e  `contacts({'firstname': 'Jack'}){..}`
- Not equals `!=`
    - put `~` before your string i.e `contacts({'firstname': '~Jack'}){..}`
- contains
    - `contacts({'firstname': 'contains(ali)'}){..}`
- like
    -  `contacts({'firstname': 'contains(ali%)'}){..}`
- null
    - `contacts({'lastname': 'null'}){..}`
- not null
    - `contacts({'lastname': '~null'}){..}`
- in
    - `contacts({'lastname': 'in(ali, fathy)'}){..}`
- not in
    - `contacts({'lastname': '~in(ali, fathy)'}){..}`
- `>,<,>=,<=`
    - `deals({'value': '>=(10)'}){..}`
    - `deals({'value': '>=(1999-02-02)'}){..}`
- ranges
    - `deals({'value': '[4, 10]'}){..}` means `4 <= value <= 10`
    - `deals({'value': ']4, 10['}){..}` means `4 < value < 10`
    - `deals({'value': '[4, 10['}){..}` means `4 <= value < 10`
    - `deals({'value': ']4, 10]'}){..}` means `4 < value <= 10`
- `or`
    - `or(ali,fathy)`
    - `or(contains(ali), contains(fathy))`
- `and`
    - `and(contains(ali), ~alii)`
