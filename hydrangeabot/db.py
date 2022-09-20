import json

from mongoengine import (
    BinaryField,
    DictField,
    Document,
    DynamicDocument,
    DynamicField,
    LazyReferenceField,
    LongField,
    StringField,
    ValidationError,
)


def validate_schema_json(string: bytes):
    try:
        json.loads(string)
    except json.JSONDecodeError:
        raise ValidationError


class User(Document):
    snowflake = LongField(required=True, primary_key=True)

    macros = DictField()


class CharacterSchema(DynamicDocument):
    creator = LazyReferenceField(User)

    name = StringField(min_length=1, max_length=32, primary_key=True)
    json = BinaryField(validation=validate_schema_json, max_bytes=4096)

    schema = DynamicField(required=True)


class Character(DynamicDocument):
    creator = LazyReferenceField(User)

    name = StringField(required=True, max_length=48)
    description = StringField(max_length=1024)
    schema = LazyReferenceField(CharacterSchema)


def db_get_user(**kwargs):
    return User.objects(**kwargs).get()  # type: ignore


def db_query_characters(**kwargs):
    return Character.objects(**kwargs)  # type: ignore
