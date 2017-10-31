from subprocess import Popen, PIPE

from crm import app


@app.cli.command()
def generate_graphql_docs():
    """
    Generates schema.graphql IDL file and the GraphQL API documentation for queries and mutations.

    requires graphdoc to be installed.

    """
    from crm import app
    sc = app.graphql_schema

    with open('./schema.graphql', "w") as f:
        f.write(str(sc))

    p = Popen(['graphdoc', '--force', '-s', './schema.graphql', '-o',
               'docs/graphqlapi'], stdout=PIPE, stderr=PIPE)

    p.communicate()[0]

    if p.returncode != 0:
        print("Failed to generate graphqlapi docs.")
        exit(1)
