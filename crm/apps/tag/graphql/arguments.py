import graphene
from graphene.types.inputobjecttype import InputObjectType


class TagArguments(InputObjectType):
    tag = graphene.String()

