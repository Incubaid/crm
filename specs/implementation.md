
# recommended flask

- flask admin
- sqlite backend (which will be loaded from toml files when starting from GIT repo)
- peewee or sqlalchemy

# or django

- with auto admin interface
- sqlite backend (which will be loaded from toml files when starting from GIT repo)

# for both

- generate graphql & rest backend
- documented rest interface (generated raml or swagger from model definition)
- IYO integration (user name/email/tel comes from IYO and gets filled in DB automatically while registering)

# phase 2

- walk over toml files which are stored in git directory structure -> mysql using the orm
- when object changes -> modify toml on git right away, git commit with username/email which did the change


