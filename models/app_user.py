import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class AppUsers(db.Model):
    __tablename__ = 'AppUsers'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String())
    address = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.Enum('user', 'super-admin', 'employee', name='role'), nullable=False, default=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    auth = db.relationship('AuthTokens', back_populates='user')

    def __init__(self, first_name, last_name, email, address, password, phone_number, role='role', active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.password = password
        self.phone_number = phone_number
        self.role = role
        self.active = active

    def new_user_obj():
        return AppUsers('', '', '', '', '', '', 'user', True)


class AppUsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'password', 'role', 'active']


user_schema = AppUsersSchema()
users_schema = AppUsersSchema(many=True)
