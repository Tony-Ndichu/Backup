"""

#app/test/test_answers.py
Handles all the tests related to answers
"""
import json
from api import create_app
from flask_testing import TestCase
from api.database.connect import conn, cur
from api.manage import tables
from tests.base import Base
import os




class TestApp(Base):

    """Contains all the methods for testing answers"""

    def post_question_for_testing_purposes(self):
        """posts question to enable testing where existing question is needed"""


        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        result = self.client.post(
            'api/v1/questions', data=json.dumps(self.sample_data7), content_type='application/json',
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

    def test_user_can_answer_question(self):
        """checks that users can add an answer"""
        self.post_question_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        answer = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        print(access_token)
        self.assertEqual(answer.status_code, 201)

    def test_user_cannot_answer_with_empty_content(self):
        """checks that user cannot add an empty answer"""
        self.post_question_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        result = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.empty_answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(result.status_code, 409)

    def test_user_can_view_questions_with_the_most_answers(self):
        """checks that user can view the most answered question"""

        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        self.post_question_for_testing_purposes()

        self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer2),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        result = self.client.get(
            'api/v1/questions/most_answered',
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(result.status_code, 200)

    def test_user_can_accept_answer_as_preffered(self):
        """checks that a user can choose and answer to be the preferred answer"""
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        accept_que=self.client.put(
            'api/v1/questions/1/answers/1/accept',
            data=json.dumps(self.answer2),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(accept_que.status_code, 200)

    def test_user_can_get_answers_to_specific_question(self):
        
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']  

        answer = self.client.get(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(answer.status_code, 200)     


    def test_user_must_enter_number_in_post_answer_uri(self):
        """checks that user doesnt do something like 'api/v1/questions/seven/answers'"""

        self.post_question_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        answer = self.client.post(
            'api/v1/questions/string/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(answer.status_code, 400)

    def test_user_must_enter_integer_in_get_answer_url(self):
        """checks that user doesnt do something like 'api/v1/questions/seven/answers'"""

        
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']  

        answer = self.client.get(
            'api/v1/questions/string/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(answer.status_code, 400)     

    def test_use_must_integers_in_uri_when_accepting_answer(self):
        """checks that user doesnt do something like 'api/v1/questions/one/answers/1/accept'"""

        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        accept_que=self.client.put(
            'api/v1/questions/one/answers/1/accept',
            data=json.dumps(self.answer2),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(accept_que.status_code, 400)

    def test_use_must_integers_in_uri_when_accepting_answer(self):
        """checks that user doesnt do something like 'api/v1/questions/1/answers/one/accept'"""

        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        accept_que=self.client.put(
            'api/v1/questions/1/answers/one/accept',
            data=json.dumps(self.answer2),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(accept_que.status_code, 400)

    def test_user_cannot_post_same_answer_twice(self):
        """checks that user cannot post exact same answer twice for the same question"""
        self.post_question_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        que = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(que.status_code, 409)


    def test_user_must_have_posted_question_to_accept_answer_as_preffered(self):
        """checks that a user can choose and answer to be the preferred answer"""
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()

        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details2),
            content_type='application/json')

        self.login2=self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(self.login_details2),
            content_type='application/json')

        result = json.loads(self.login2.data.decode())
        access_token = result['access_token']

        accept_que=self.client.put(
            'api/v1/questions/1/answers/1/accept',
            data=json.dumps(self.answer2),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(accept_que.status_code, 401)