from crm import app

from sqlalchemy_utils import create_database, database_exists


@app.cli.command()
def createdb():
    """
    Create DB    
    """
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    print("DB created.")
