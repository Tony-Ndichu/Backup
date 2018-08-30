"""

#app/test/test_comments.py
Handles all the tests related to answers
"""
import json
from api import create_app
from flask_testing import TestCase
from api.database.connect import conn, cur
from api.manage import tables
import os
from tests.base import Base

class TestApp(Base):

    """Contains all the methods for testing answers"""

    def post_question_for_testing_purposes(self):
        """posts question to enable testing where existing question is needed"""


        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        result = self.client.post(
            'api/v1/questions', data=json.dumps(self.sample_data_que), content_type='application/json',
             headers = {'Authorization' : 'Bearer '+ access_token })
        return result


    def post_answer_for_testing_purposes(self):
        """posts answer to enable testing where existing answer is needed"""

        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        result = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json', headers = {'Authorization' : 'Bearer '+ access_token })

        return result

    def test_user_can_add_comment(self):
        """checks that users can add an answer"""
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        comment = self.client.post(
            'api/v1/questions/1/answers/1/comments',
            data=json.dumps(self.comment),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(comment.status_code, 201)

    def test_user_cannot_add_comment_to_an_answer_taht_doesnt_exist(self):
        """checks that answer exists inorder for comment to be added"""
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        comment = self.client.post(
            'api/v1/questions/1/answers/3/comments',
            data=json.dumps(self.comment),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(comment.status_code, 404)

    def test_user_must_enter_answer_id_as_integer_in_uri(self):
        """checks that users cant do something like 'api/v1/questions/1/answers/one/comments"""
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        comment = self.client.post(
            'api/v1/questions/1/answers/one/comments',
            data=json.dumps(self.comment),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(comment.status_code, 400)
