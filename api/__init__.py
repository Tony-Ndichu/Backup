"""
# app/api/__init__.py
Handles create_app method and blueprint registration
"""

from flask import Flask
from .config import CONFIG
from flask_jwt_extended import JWTManager
from datetime import timedelta
from .database.connect import conn, cur
from flask_cors import CORS


jwt = JWTManager()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    query = "SELECT * FROM tokens WHERE jti = %s;"
    fetch_query = cur.execute(query, [jti])
    result = cur.fetchone()

    return result

def create_app(config):
	"""This is the application factory"""
	app = Flask(__name__)
	app.config.from_object(CONFIG[config])
	app.url_map.strict_slashes = False
	app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
	jwt.init_app(app)


	from .comments.views import COMMENT_BLUEPRINT
	from .questions.views import QUESTION_BLUEPRINT
	from .answers.views import ANSWER_BLUEPRINT
	from .users.views import USER_BLUEPRINT
	app.register_blueprint(QUESTION_BLUEPRINT)
	app.register_blueprint(ANSWER_BLUEPRINT)
	app.register_blueprint(USER_BLUEPRINT)
	app.register_blueprint(COMMENT_BLUEPRINT)
	CORS(app)
	return app


