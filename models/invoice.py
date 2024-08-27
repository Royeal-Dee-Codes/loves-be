import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Invoice(db.Model):
    __tablename__ = 'Invoice'

    invoice_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    total_amount = db.Column(db.Float(), nullable=False)
    issued_date = db.Column(db.DateTime(), nullable=False)
    payment_status = db.Column(db.Boolean(), nullable=False, default=False)

    appt_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Appointment.appt_id'), nullable=False)

    def __init__(self, total_amount, issued_date, payment_status=False):
        self.total_amount = total_amount
        self.issued_date = issued_date
        self.payment_status = payment_status

    def new_invoice_obj():
        return Invoice('', '', False)


class InvoicesSchema(ma.Schema):
    class Meta:
        fields = ['invoice_id', 'total_amount', 'issued_date', 'payment_status']

    # appt_id = ma.fields.Nested('AppointmentSchema', exclude=['appt_id'])


invoice_schema = InvoicesSchema()
invoices_schema = InvoicesSchema(many=True)
