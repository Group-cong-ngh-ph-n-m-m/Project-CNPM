from infrastructure.databases.mssql import init_mssql
from infrastructure.models import todo_model, user_model, subject_model, student_model, tutor_profile_model, admin_model
from infrastructure.models import service_model, booking_model, conversation_model, message_model, rating_model, review_model, complaint_model
from infrastructure.models import moderation_action_model

def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base