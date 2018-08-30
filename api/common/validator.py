"""

# app/api/common/validator.py
This module contains all the cide used to validate input
It is used by both the question and answer views and models
"""
import psycopg2
from ..database.connect import conn, cur
import re
from flask import request



def check_email_validity(email):
    """ensure that the email input is valid"""
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    if not re.match(email_regex, email):
        return {
                'Status': 'Error',
                'message': 'Ooops! {} is not a valid email address'.format(email) }, 400

def check_text_validity(text):
    text_regex =  re.compile(r"(^[A-Za-z]+$)")

    if not re.match(text_regex, text):
        return {
                'Status': 'Error',
                'message': 'Ooops! {} is not a valid input'.format(text) }, 400


def check_if_already_exists(list_name, title):
    """"
    check if the question title or description
    already exists in storage
    """

    for item in list_name:
        if item[2] == title:
            return 'Sorry, This title has already been used in another question'



def check_for_answer(answer):
    """check if a similar answer exists"""
    answer_list = []
    conn
    que = cur.execute("SELECT * FROM answers")

    try:
        que
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
        conn
        cur

    result = cur.fetchall()    

    for item in result:
        if item[3] == answer:
            return True


def question_verification(title, description):
    """

    check the quality of questions sent such as 
    the length of the input and character type
    """
    if len(title) < 1:
        return 'You cannot post an empty title, Please add a title'
    if len(description) < 1:
        return 'You cannot post an empty description, Please add a description'
    if title.isdigit():
        return 'You cannot post a title with digits only, Please describe with some words'
    if description.isdigit():
        return 'You cannot post a description with digits only, Please describe with some words'

def make_save_dict(arg1, arg2, arg3):

    new_dict = dict(arg1=arg1, arg2=arg2, arg3=arg3)

    return new_dict

def check_quality(item):
    """check answer quality"""

    if len(item) < 1:
        return 'Too Short, Please add more input'


def find_answers_to_a_question(list_name, question_id):
    """find all the answers posted to a question"""

    my_items = [element for element in list_name if element[
        'question_id'] == question_id]

    if my_items:
        return my_items
    return False


def check_if_user_exists(user_list, username, email):
    """check if the username or email has already been used"""

    for item in user_list:
        if item[3] == username:
            return 'Sorry, This username has already been taken'
        if item[4] == email:
            return 'Sorry, This email is already in use'


def user_detail_verification(firstname, lastname, username):
    """check if details inputed are of a valid type"""
    if len(firstname) < 3 or len(lastname) < 3 or len(username) < 3:
        return 'Too short, please add more characters'
    if len(firstname) > 15 or len(lastname) > 15 or len(username) > 15:
        return 'Too long, please remove some characters'
    if firstname.isdigit() or lastname.isdigit() or lastname.isdigit():
        return 'This cannot be digits'

def check_using_id(list_name, other_id):
    """use the relevant id to find item in a list"""
    for item in list_name:
        if item[0] == other_id:
            return item


def insert_to_blacklist():
    auth_token = auth_header.split(" ")[1]  
    cur.execute("INSERT into tokens(token) values(%s)",[auth_token])
    conn.commit() 

    return "Logout successful"

def check_if_token_is_invalid():

    auth_header = request.headers.get(1)
    print(auth_header)
    if not auth_header:
        return "You have no Authorization"

    auth_token = auth_header.split("Header ")[1]        
    fetch_question = "SELECT * FROM tokens WHERE token = %s;"
    fetched_question = cur.execute(fetch_question, [auth_token])
    result = cur.fetchall()

    if result:
        return "You have no access, please login again"
