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


class TestUsers(Base):
    """contains the test methods"""
    def test_user_can_register(self):
        req = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details_true),
            content_type='application/json')

        self.assertEqual(req.status_code, 201)

    def test_user_registration_details(self):
        """ensures user registers with valid details"""
        req1 = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details_false_1),
            content_type='application/json')

        req2 = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details_false_2),
            content_type='application/json')

        req3 = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details_false_3),
            content_type='application/json')

        req4 = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details_false_4),
            content_type='application/json')

        req5 = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details_false_5),
            content_type='application/json')

        self.assertEqual(req1.status_code, 409)
        self.assertEqual(req2.status_code, 409)
        self.assertEqual(req3.status_code, 409)
        self.assertEqual(req4.status_code, 400)
        self.assertEqual(req5.status_code, 400)




    def test_user_cannot_register_with_existing_credentials(self):
        req = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details),
            content_type='application/json')

        req2 = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details),
            content_type='application/json')

        self.assertEqual(req2.status_code, 409)

    def test_user_can_login(self):

        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details),
            content_type='application/json')    


        req1 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(self.login_details),
            content_type='application/json')

        req3 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(self.login_details_false2),
            content_type='application/json')

        self.assertEqual(req1.status_code, 200)
        self.assertEqual(req3.status_code, 404)



    # def test_user_can_logout(self):

    #     que = self.client.post(
    #         '/api/v1/auth/login',
    #         data=json.dumps(self.login_details),
    #         content_type='application/json')

    #     result = json.loads(que.data.decode())

    #     req = self.client.post(
    #         '/api/v1/auth/logout',
    #         content_type='application/json')

    #     self.assertEqual(req.status_code, 200)