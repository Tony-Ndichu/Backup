"""
#app/api/answers/view.py
This is the module that handles answers and their methods
"""
from datetime import datetime
from flask import Flask, Blueprint
from flask_restful import reqparse, Api, Resource
from ..common import validator
from ..models.answer import AnswerModel
from ..models.question import QuestionModel
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


APP = Flask(__name__)


ANSWER_BLUEPRINT = Blueprint('answer', __name__)
API = Api(ANSWER_BLUEPRINT, prefix='/api/v1')


class Answer(Resource):
    """This class deals with posting answers and getting answers to specific questions"""
    parser = reqparse.RequestParser()
    parser.add_argument('answer', type=str, required=True,
                        help='Please enter an answer.')

    @classmethod
    @jwt_required
    def post(cls, questionid):
        """Handles posting of answers"""

        try:
            val = int(questionid)
        except ValueError:
            return { "message" : "Sorry, questionid must be a number or an integer" }, 400

        data = cls.parser.parse_args()


        QUESTION_LIST = QuestionModel.get_questions()

        check_question = validator.check_using_id(
            QUESTION_LIST, int(questionid))

        if not check_question:
            return {'message': 'Oops, that question is missing, you cant add answers to it'}, 404

        check_answer = validator.check_for_answer(data['answer'])

        if check_answer:
            return {"message":
                    "Please enter a different answer, you cannot enter the same answer twice"}, 409

        check_quality = validator.check_quality(data['answer'])

        if check_quality:
            return {"message": check_quality}, 409

        current_user_id = get_jwt_identity()

        make_save_dict = validator.make_save_dict(current_user_id, questionid, data['answer'])

        save_answer = AnswerModel.save_answer(make_save_dict)

        if save_answer:
            message = {"message": "Success!! Your answer has been added"}, 201

        return message

    @classmethod
    def get(cls, questionid):
        """Handles getting answers for a specific question"""

        try:
            val = int(questionid)
        except ValueError:
            return { "message" : "Sorry, questionid must be a number or an integer" }, 400

        check_answer = AnswerModel.get_answers(questionid)

        if check_answer:

            answer_list=[]

            for i in check_answer:
                answer_dict = dict(answer_id=i[0], user_id=i[1], question_id=i[2], answer_body=i[3])
                answer_list.append(answer_dict)

            return { "message" : "Success!! Here are your answers" , "list" :  answer_list }, 200
        return {"message": "Sorry, this question has no answers at the moment."}, 404


class AcceptAnswer(Resource):
    """Handles updating an answer's status"""
    @classmethod
    @jwt_required
    def put(cls, question_id, answer_id):
        """Handles accepting an answer"""

        try:
            val = int(question_id)
        except ValueError:
            return { "message" : "Sorry, questionid must be a number or an integer" }, 400

        try:
            val = int(answer_id)
        except ValueError:
            return { "message" : "Sorry, questionid must be a number or an integer" }, 400

        current_user_id = get_jwt_identity()
        confirm_that_user_asked_que = QuestionModel.check_who_posted(
            current_user_id, question_id)

        if confirm_that_user_asked_que:
            return {"message": "Sorry, you cant accept this answer since you didnt post the question"}, 401

        check_if_already_accepted = AnswerModel.check_if_already_accepted(question_id)

        if check_if_already_accepted:
            return {"message": check_if_already_accepted}, 409

        accept_answer = AnswerModel.accept_answer(answer_id)

        if accept_answer:
            return {"message": "Success!! You have accepted this answer"}, 200


API.add_resource(Answer, "/questions/<questionid>/answers")
API.add_resource(
    AcceptAnswer, "/questions/<question_id>/answers/<answer_id>/accept")

if __name__ == '__main__':
    APP.run()
