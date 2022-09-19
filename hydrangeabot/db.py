from mongoengine import DictField, Document, LongField


class Users(Document):
    snowflake = LongField(required=True)
    macros = DictField()


def _get_user(**kwargs):
    return Users.objects(**kwargs).get()  # type: ignore
