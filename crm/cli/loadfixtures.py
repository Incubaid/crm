from crm import app
from crm.fixtures import generate_fixtures


@app.cli.command()
def loadfixtures():
    """
    populate DB with Test/Random Data 
    """
    generate_fixtures()
