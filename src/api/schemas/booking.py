from marshmallow import Schema, fields

class BookingRequestSchema(Schema):
    student_id = fields.Int(required=True)
    tutor_id = fields.Int(required=True)
    subject_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    status = fields.Str(required=True)

class BookingResponseSchema(Schema):
    id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    tutor_id = fields.Int(required=True)
    subject_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    status = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
