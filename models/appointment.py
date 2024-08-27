import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Appointment(db.Model):
    __tablename__ = 'Appointment'

    appt_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appt_date = db.Column(db.DateTime(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('AppUsers.user_id'), nullable=False)
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Service.service_id'), nullable=False)

    # user = db.relationship('AppUsers', back_populates='user_id')
    # service = db.relationship('Service', back_populates='service_id')

    def __init__(self, appt_date, active, user_id, service_id):
        self.appt_date = appt_date
        self.active = active
        self.user_id = user_id
        self.service_id = service_id

    def new_appt_obj():
        return Appointment('', True, '', '')


class AppointmentsSchema(ma.Schema):
    class Meta:
        fields = ['appt_date', 'active', 'user_id', 'service_id']

        user = ma.fields.Nested('AppUsersSchema', exclude=['user'])
        service = ma.fields.Nested('ServicesSchema', exclude=['service_id'])


appt_schema = AppointmentsSchema()
