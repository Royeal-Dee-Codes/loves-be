import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class AuthTokens(db.Model):
    __tablename__ = 'AuthTokens'

    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('AppUsers.user_id'))
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Employees.employee_id'))
    expiration = db.Column(db.DateTime(), nullable=False)

    user = db.relationship('AppUsers', back_populates='auth')
    employee = db.relationship('Employees', back_populates='employee')

    def __init__(self, expiration, user_id=None, employee_id=None):
        self.expiration = expiration
        self.user_id = user_id
        self.employee_id = employee_id


class AuthTokensSchema(ma.Schema):
    class Meta:
        fields = ['auth_token', 'user', 'employee', 'expiration']

    user = ma.fields.Nested('AppUsersSchema', only=['user_id', 'first_name', 'last_name', 'email', 'role', 'active'])
    employee = ma.fields.Nested('Employees', only=['employee_id', 'first_name', 'last_name', 'phone_number', 'email', 'role'])


auth_token_schema = AuthTokensSchema()
