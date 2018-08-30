"""

#app/test/test_answers.py
Handles all the tests related to answers
"""
import json
from api import create_app
from flask_testing import TestCase
from api.database.connect import conn, cur
import os
from api.manage import tables
from tests.base import Base

class TestApp(Base):

    """Contains all the methods for testing questions"""

    def post_for_testing_purposes(self):
        """post question to enable testing"""
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        result = self.client.post(
            'api/v1/questions',
            data=json.dumps(self.sample_data7),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })
        return result

    def test_get_all_questions(self):
        """checks that a 200 status code is given when questions are available"""

        self.post_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        response = self.client.get('api/v1/questions', headers = {'Authorization' : 'Bearer '+ access_token })
        self.assertEqual(response.status_code, 200)

    def test_get_all_questions_status_code_when_questions_exist(self):
        """checks that a successful 200 status code is given when questions exist"""

        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        self.client.post(
            'api/v1/questions',
            data=json.dumps(self.sample_data7),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        response = self.client.get('/api/v1/questions', headers = {'Authorization' : 'Bearer '+ access_token })
        self.assertEqual(response.status_code, 200)

    def test_user_can_post_question(self):
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        print(access_token)

        que = self.client.post(
            'api/v1/questions',
            data=json.dumps(self.sample_data7),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(que.status_code, 201)

    def test_user_cannot_post_same_question_title_twice(self):
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        self.client.post(
            'api/v1/questions',
            data=json.dumps(self.sample_data7),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        que=self.client.post(
            'api/v1/questions',
            data=json.dumps(self.sample_data7),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(que.status_code, 409)


    def test_post_question_with_no_title(self):
        """checks that user cannot post a question without a title"""

        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        que = self.client.post(
            '/api/v1/questions', headers = {'Authorization' : 'Bearer '+ access_token }, 
            data=self.sample_data1)

        result = json.loads(que.data.decode())
        self.assertEqual(
            result['message'], {'title': 'Please enter a title.'})
        self.assertEqual(que.status_code, 400)

    def test_post_question_with_no_description(self):
        """checks that a user cannot post a question without a description"""

        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        que = self.client.post(
            '/api/v1/questions',
            data=self.sample_data2, headers = {'Authorization' : 'Bearer '+ access_token })

        result = json.loads(que.data.decode())
        self.assertEqual(
            result['message'], {'description': 'Please enter a description.'})
        self.assertEqual(que.status_code, 400)

    def test_post_question_with_empty_string_title(self):
        """checks that user cannot post an empty string title"""
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        que = self.client.post(
            '/api/v1/questions',
            data=self.sample_data3, headers = {'Authorization' : 'Bearer '+ access_token })

        result = json.loads(que.data.decode())
        self.assertEqual(
            result['message'], 'You cannot post an empty title, Please add a title')
        self.assertEqual(que.status_code, 409)

    def test_post_question_with_empty_string_description(self):
        """checks that user cannot post an empty string description"""
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        que = self.client.post(
            '/api/v1/questions',
            data=self.sample_data4, headers = {'Authorization' : 'Bearer '+ access_token })

        result = json.loads(que.data.decode())
        self.assertEqual(
            result['message'], 'You cannot post an empty description, Please add a description')
        self.assertEqual(que.status_code, 409)

    def test_post_question_where_title_is_only_digits(self):
        """checks that user cannot post a title with digits only"""

        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        que = self.client.post(
            '/api/v1/questions',
            data=self.sample_data5, headers = {'Authorization' : 'Bearer '+ access_token })

        result = json.loads(que.data.decode())
        self.assertEqual(
            result['message'],
            'You cannot post a title with digits only, Please describe with some words')
        self.assertEqual(que.status_code, 409)

    def test_post_question_where_description_is_only_digits(self):
        """checks that user cannot post a description with digits only"""

        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        que = self.client.post(
            '/api/v1/questions',
            data=self.sample_data6, headers = {'Authorization' : 'Bearer '+ access_token })

        result = json.loads(que.data.decode())
        self.assertEqual(
            result['message'],
            'You cannot post a description with digits only, Please describe with some words')
        self.assertEqual(que.status_code, 409)

    def test_fetch_a_question(self):
        """checks that user can fetch a specific question"""
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        self.post_for_testing_purposes()

        response = self.client.get('/api/v1/questions/1', headers = {'Authorization' : 'Bearer '+ access_token })
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_question(self):
        """checks that user can delete a specific question"""
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        self.post_for_testing_purposes()

        result = self.client.delete(
            'api/v1/questions/1',
            content_type="application/json", headers = {'Authorization' : 'Bearer '+ access_token })

        self.assertEqual(result.status_code, 200)



    def test_user_can_fetch_all_his_or_her_questions(self):
        """get all questions belonging to the logged in user"""
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        self.post_for_testing_purposes()

        response = self.client.get('/api/v1/auth/questions', headers = {'Authorization' : 'Bearer '+ access_token })
        self.assertEqual(response.status_code, 200)


