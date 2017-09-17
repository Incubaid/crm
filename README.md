## Motivation

We are doing our ITO = Internal Token Offering we need a CRM to manage the users/tasks/projects.
We are aiming for simplicity and thus this tool can be customized and offered for people whom certainly will like it.
We want also any record in DB to have a simple UID (4 chars only, lower case number/letter e.g. 5bhs) to simplify passing
UIDs between users.


#### Problems with current tools
- Too difficult to get [Teal organization](http://www.reinventingorganizationswiki.com/Teal_Organizations) features in
- Either too complex, too expensive, ugly or not what we need.
- No [IYO](https://itsyou.online) integration
    - Users info like (username, email, tel, .. ) **Must** come from [IYO](https://itsyou.online)
- No [Git](https://git-scm.com/) integration
  - When DB changes, theses changes should go to [Redis](https://redis.io/) cache
    https://redis.io/
   - Then these changes **MUST** be committed in the json/toml files in a git repo
    with the proper info ```user_name, user_email, object name (i.e task), uid, epoch```

## Index

#### Specs
- [Models](api/crm/docs/Models.md)

#### API

- [Installation](api/crm/docs/Installation.md)
- [Django Admin interface](api/crm/docs/Admin.md)
- [Graphql](api/crm/docs/Graphql.md)
