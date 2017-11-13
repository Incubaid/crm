from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.passport.models import Passport


class PassportType(SQLAlchemyObjectType):

    class Meta:
        model = Passport
