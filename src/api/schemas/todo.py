from marshmallow import Schema, fields

class TodoRequestSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)

class TodoResponseSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True) 

class SubjectRequestSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)

class SubjectResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

class TutorProfileRequestSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)

class TutorProfileResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

class MessageRequestSchema(Schema):
    content = fields.Str(required=True)
    sender_id = fields.Int(required=True)
    receiver_id = fields.Int(required=True)
    
class MessageResponseSchema(Schema):
    id = fields.Int(required=True)
    content = fields.Str(required=True)
    sender_id = fields.Int(required=True)
    receiver_id = fields.Int(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

class ConversationRequestSchema(Schema):
    sender = fields.Str(required=True)
    receiver = fields.Str(required=True)
    message = fields.Str(required=True)

class ConversationResponseSchema(Schema):
    id = fields.Int(required=True)
    sender = fields.Str(required=True)
    receiver = fields.Str(required=True)
    message = fields.Str(required=True)
    timestamp = fields.Raw(required=True)

class RatingRequestSchema(Schema):
    user_id = fields.Int(required=True)
    item_id = fields.Int(required=True)
    score = fields.Float(required=True)
    comment = fields.Str(required=False)

class RatingResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    item_id = fields.Int(required=True)
    score = fields.Float(required=True)
    comment = fields.Str(required=False)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

class ReviewRequestSchema(Schema):
    user_id = fields.Int(required=True)
    item_id = fields.Int(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    rating = fields.Float(required=False)  # optional

class ReviewResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    item_id = fields.Int(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    rating = fields.Float(required=False)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

