from mongoengine import (BooleanField, Document, EmailField, IntField,
                         ReferenceField, StringField, connect)

from app.config import settings

connect(db=settings.mongo_db_name, host=settings.mongo_url)


class User(Document):
    email_address = EmailField(required=True, unique=True)
    password = StringField(required=True)
    is_admin = BooleanField(default=False)


class UserPreference(Document):
    user = ReferenceField(User, required=True, unique=True)
    preferred_location = StringField(required=True)
    min_rooms = IntField(required=True)
    max_rent = IntField(required=True)
