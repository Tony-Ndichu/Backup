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



class Base(TestCase):
    """contains config for testing"""

    def create_app(self):
        """sets config to testing"""
        self.app = create_app('testing')
        return self.app

    def setUp(self):
        tables("drop")
        tables("create")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()
        
        #QUESTION TEST DATA

        self.sample_data1 = {
            'description': 'A tuple is a python data structure'
        }

        self.sample_data2 = {
            'title': 'What is a title?'
        }

        self.sample_data3 = {
            'title': '',
            'description': 'A tuple is a python data structure'

        }

        self.sample_data4 = {
            'title': 'What is a title?',
            'description': ''

        }

        self.sample_data5 = {
            'title': '12345',
            'description': 'A tuple is a python data structure'

        }

        self.sample_data6 = {
            'title': 'What is a title?',
            'description': '12345'

        }

        self.sample_data7 = {

            'title': 'What is a tuple?',
            'description': 'A tuple is a python data structure'
        }

        self.signup_details = {
            "first_name" : "John",
            "last_name" : "Doe",
            "username" : "josdhndoe",
            "email" : "johndsdoe@gmail.com",
            "password" : "absdcd1234"
            }

        self.signup_details_true = {
            "first_name" : "Tommy",
            "last_name" : "Hilfiger",
            "username" : "tommyfiger",
            "email" : "tommy@gmail.com",
            "password" : "absdcd1234"
            } 

        self.login_details = {            
            "username" : "josdhndoe",
            "password" : "absdcd1234"           
            } 

         ##end of questions test data

         #ANSWER TEST DATA
        self.answer = {
            "answer": "This is a sample answer"
        }

        self.answer2 = {
            "answer": "This is another sample answer"
        }


        self.empty_answer = {
            'answer': ""
        }

        self.signup_details2 = {
            "first_name" : "Jane",
            "last_name" : "Doe",
            "username" : "janedoe",
            "email" : "janedoe@gmail.com",
            "password" : "absdcd1234"
            } 

        #end of answer test data

        #COMMENT TEST DATA
        self.comment = {
            "comment" : "This is a sample comment"
        }

        self.sample_data_que = {
            'title': 'What is a tuple?',
            'description': 'A tuple is a python data structure'
        }


        #end of comment test data

        #USER TEST DATA

        self.signup_details_false_1 = {
            "first_name" : "J",
            "last_name" : "Doe",
            "username" : "false",
            "email" : "false1@gmail.com",
            "password" : "absdcd1234"
            } 

        self.signup_details_false_2 = {
            "first_name" : "John",
            "last_name" : "D",
            "username" : "false",
            "email" : "false2@gmail.com",
            "password" : "absdcd1234"
            } 

        self.signup_details_false_3 = {
            "first_name" : "Johntftfghjjhvvjvjhvjvj",
            "last_name" : "Doe",
            "username" : "false",
            "email" : "false3@gmail.com",
            "password" : "absdcd1234"
            } 

        self.signup_details_false_4 = {
            "first_name" : "1234",
            "last_name" : "Doe",
            "username" : "false",
            "email" : "false4@gmail.com",
            "password" : "absdcd1234"
            } 

        self.signup_details_false_5 = {
            "first_name" : "John",
            "last_name" : "5678",
            "username" : "false",
            "email" : "false5@gmail.com",
            "password" : "absdcd1234"
            } 

        self.login_details = {            
            "username" : "josdhndoe",
            "password" : "absdcd1234"           
            } 

        self.login_details_false1 = {            
            "username" : "josdhndoe",
            "password" : "absdcd"           
            } 

        self.login_details_false2 = {            
            "username" : "josd",
            "password" : "absdcd1234"           
            } 
            
        self.login_details2 = {            
            "username" : "janedoe",
            "password" : "absdcd1234"           
            } 


        #end of user test data

        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details),
            content_type='application/json')

        self.que = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(self.login_details),
            content_type='application/json')


    def tearDown(self):
        self.app_context.pop()    
        tables("drop")