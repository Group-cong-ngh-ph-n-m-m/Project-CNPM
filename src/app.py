from flask import Flask, jsonify
from api.swagger import spec
from api.controllers.todo_controller import bp as todo_bp
from api.controllers.user_controller import bp as user_bp
from api.controllers.subject_controllers import bp as subject_bp
from api.controllers.tutor_profile_controllers import bp as tutor_profile_bp
from api.controllers.message_controllers import bp as message_bp
from api.controllers.admin_controller import bp as admin_bp
from api.controllers.booking_controllers import bp as booking_bp
from api.controllers.complaint_controllers import bp as complaint_bp
from api.controllers.conversation_controllers import bp as conversation_bp
from api.controllers.rating_controllers import bp as rating_bp
from api.controllers.review_controllers import bp as review_bp
from api.controllers.service_controller import bp as service_bp
from api.controllers.video_controller import bp as video_bp
from api.middleware import middleware
from api.responses import success_response
from infrastructure.databases import init_db
from config import Config
from flasgger import Swagger
from config import SwaggerConfig
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)
    Swagger(app)
    # Đăng ký blueprint trước
    app.register_blueprint(todo_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(subject_bp)
    app.register_blueprint(tutor_profile_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(complaint_bp)
    app.register_blueprint(rating_bp)
    app.register_blueprint(conversation_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(video_bp) 
    # Thêm Swagger UI blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Todo API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    init_db(app)

    # Register middleware
    middleware(app)

    # Register routes
    # Example: app.add_url_rule('/example', view_func=example_view)
    # Tự động quét tất cả các route đã đăng ký
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith(('todo.', 'user.', 'subject.', 'tutor_profile.', 'message.', 'admin.', 'booking.', 'complaint.', 'conversation.', 'rating.', 'review.', "service.", "video.",)):
                view_func = app.view_functions[rule.endpoint]
                print(f"Adding path: {rule.rule} -> {view_func}")
                spec.path(view=view_func)

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=6868, debug=True)
