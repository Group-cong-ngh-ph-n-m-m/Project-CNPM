# api/schemas/complaint.py
from marshmallow import Schema, fields

class ComplaintRequestSchema(Schema):
    filed_by_user_id = fields.Int(required=True)
    target_user_id = fields.Int(required=True)
    booking_id = fields.Int(required=True)
    subject = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)

class ComplaintResponseSchema(Schema):
    id = fields.Int(required=True)
    filed_by_user_id = fields.Int(required=True)
    target_user_id = fields.Int(required=True)
    booking_id = fields.Int(required=True)
    subject = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    resolved_at = fields.Raw(required=False)
