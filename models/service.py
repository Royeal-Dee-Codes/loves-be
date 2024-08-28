import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Service(db.Model):
    __tablename__ = 'Service'

    service_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('AppUsers.user_id'), nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('AppUsers.user_id'))

    def __init__(self, service_name, description, price, user):
        self.service_name = service_name
        self.description = description
        self.price = price
        self.user = user

    def new_service_obj():
        return Service('', '', False, '')


class ServicesSchema(ma.Schema):
    class Meta:
        fields = ['service_id', 'service_name', 'description', 'price', 'user']

        user = ma.fields.Nested('AppUsersSchema', exclude=['user'])


service_schema = ServicesSchema()
services_schema = ServicesSchema(many=True)
