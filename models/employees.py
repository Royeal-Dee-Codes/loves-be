import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Employees(db.Model):
    __tablename__ = 'Employees'

    employee_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    role = db.Column(db.String(), nullable=False, default='employee')

    auth = db.relationship('AuthTokens', back_populates='employee')

    def __init__(self, first_name, last_name, email, password, phone_number, role='employee', active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.role = role
        self.active = active

    def new_emp_obj():
        return Employees('', '', '', '', '', 'employee', True)


class EmployeesSchema(ma.Schema):
    class Meta:
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone_number', 'active', 'role']


employee_schema = EmployeesSchema()
employees_schema = EmployeesSchema(many=True)
