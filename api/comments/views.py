"""
#app/api/answers/view.py
This is the module that handles answers and their methods
"""
from datetime import datetime
from flask import Flask, Blueprint
from flask_restful import reqparse, Api, Resource
from ..models.answer import AnswerModel
from ..models.comment import CommentModel
from ..common import validator
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


APP = Flask(__name__)


COMMENT_BLUEPRINT = Blueprint('comment', __name__)
API = Api(COMMENT_BLUEPRINT, prefix='/api/v1')


class Comment(Resource):
    """This class deals with posting answers and getting answers to specific questions"""
    parser = reqparse.RequestParser()
    parser.add_argument('comment', type=str, required=True,
                        help='Please enter a comment.')

    @classmethod
    @jwt_required
    def post(cls, questionid, answerid):
        """Handles posting of answers"""

        try:
            val = int(answerid)
        except ValueError:
            return { "message" : "Sorry, answerid must be a number or an integer" }, 400

        data = cls.parser.parse_args()


        ANSWER_LIST = AnswerModel.get_answers()

        check_question = validator.check_using_id(
            ANSWER_LIST, int(answerid))

        if not check_question:
            return {'message': 'Oops, that answer is missing, you cant add comments to it'}, 404

        check_quality = validator.check_quality(data['comment'])

        if check_quality:
            return {"message": check_quality}, 409

        current_user_id = get_jwt_identity()

        make_save_dict = validator.make_save_dict(current_user_id, int(answerid), data['comment'])


        save_comment = CommentModel.save_comment(make_save_dict)

        if save_comment:
            message =  {"message": "Success!! Your comment has been added"}, 201

        return message

API.add_resource(Comment, "/questions/<questionid>/answers/<answerid>/comments")

if __name__ == '__main__':
    APP.run()
