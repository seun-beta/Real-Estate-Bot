from mongoengine import Document, IntField, StringField, connect

from app.config import settings

connect(db=settings.mongo_db_name, host=settings.mongo_url)


class Property(Document):
    rooms = IntField(required=True)
    location = StringField(required=True)
    rent = IntField(required=True)
