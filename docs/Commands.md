## Commands
- CRM has set of custom commands to make your life easier dealing with the app
To list all supported commands, use `flask --help`

```
Usage: flask [OPTIONS] COMMAND [ARGS]...

  This shell command acts as general utility script for Flask applications.

  It loads the application configured (through the FLASK_APP environment
  variable) and then provides commands either provided by the application or
  Flask itself.

  The most useful commands are the "run" and "shell" command.

  Example usage:

    $ export FLASK_APP=hello.py
    $ export FLASK_DEBUG=1
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  createdb               Create DB
  db                     Perform database migrations.
  dumpcache              Dump root objects in Cache We support only...
  dumpdata               Dump data table models into filesystem.
  generate_graphql_docs  Generates schema.graphql IDL file and the...
  loaddata               Load tables with data from filesystem.
  loadfixtures           populate DB with Test/Random Data
  mailer                 Start mailin/out services.
  run                    Runs a development server.
  shell                  Runs a shell in the app context.
  syncdata               Sync Cached DB changes in Redis to file...

```

- To get help about some command use `flask {command} --help` forexample to get more info about `flask db` which
deals with DB migrations use `flask db --help` you'll get something like
```
Usage: flask db [OPTIONS] COMMAND [ARGS]...

  Perform database migrations.

Options:
  --help  Show this message and exit.

Commands:
  branches   Show current branch points
  current    Display the current revision for each...
  downgrade  Revert to a previous version
  edit       Edit a revision file
  heads      Show current available heads in the script...
  history    List changeset scripts in chronological...
  init       Creates a new migration repository.
  merge      Merge two revisions together, creating a new...
  migrate    Autogenerate a new revision file (Alias for...
  revision   Create a new revision file.
  show       Show the revision denoted by the given...
  stamp      'stamp' the revision table with the given...
  upgrade    Upgrade to a later version

```

## Add Your custom command

- All custom commands goes in package `crm.cli`
- Add a new module for your command
    - Inside your module, put a function with the command logic you want
    - surround your command function with a docorator ```@app.cli.command()```
    - The command will get exposes automatically by `flask {function_name}`
    - Don't forget to add doc strings to document your command, they are gonna be exposed in `flask --help` automatically
- Example `crm.cli.loadfixtures.py` which exposes a command called `loadfixtures`
    ```python
    @app.cli.command()
    def loadfixtures():
        generate_fixtures()
    ```
