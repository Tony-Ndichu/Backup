""""

#app/api/models/question.py
This is the question model
"""
import psycopg2
from ..database.connect import conn, cur


class QuestionModel():
    """this class handles question-related operations"""

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id

    def turn_to_question_dict(list):
        question_list=[]

        for item in list:
            question_dict = dict(question_id=item[0], user_id = item[1], title = item[2], description = item[3] )
            question_list.append(question_dict)

        return question_list

    def get_questions(*args):

        question_list = []

        if args is not None:
            for current_user_id in args:
                fetch_user_questions = "SELECT * FROM questions WHERE user_id = %s;"
                fetched_questions = cur.execute(
                    fetch_user_questions, [current_user_id])
                result = cur.fetchall()



        que = cur.execute("SELECT * FROM questions")

        try:
            que
        except (Exception, psycopg2.DatabaseError) as error:
            print (error)
            conn
            cur

        result = cur.fetchall()


        for i in result:
            question_list.append(i)

        return question_list

    def save_to_db(self):
        """save new qestion"""

        data = dict(userid=self.user_id, title=self.title,
                    descr=self.description)

        submit = cur.execute("""INSERT INTO questions (user_id, title, description) VALUES 
                    (%(userid)s, %(title)s, %(descr)s)""", data)

        conn.commit()

        return "Successfully added question"

    def delete_question_and_its_answers(queid):
        """Delete a question"""

        delete_que = "DELETE FROM questions WHERE id = %s;"
        delete_answers ="DELETE FROM answers WHERE question_id = %s"
        cur.execute(delete_que, [queid])
        cur.execute(delete_answers, [queid])
        conn.commit()

    def check_who_posted(current_user_id, questionid):
        print(current_user_id)
        fetch_question = "SELECT * FROM questions WHERE id = %s and user_id = %s"
        fetched_question = cur.execute(fetch_question, [questionid, current_user_id])
        result = cur.fetchall()

        if len(result) < 1:
            return "Sorry, you can't delete this question, only owner has permission"

    def most_answered():

        most_answered =[]
        final_result = []

        que = cur.execute("SELECT question_id, COUNT(id) FROM answers GROUP BY question_id ORDER BY COUNT(id) DESC ")

        result = cur.fetchall()

        for i in result:
            if i[1] == 0:
                return {"message" : "Sorry, none of the questions have any answers at the moment" }
            most_answered.append(dict(question_id=i[0], no_of_answers=i[1]))

        questionid = most_answered[0]['question_id']
        no_of_answers = most_answered[0]['no_of_answers']

        fetch_question = "SELECT * FROM questions WHERE id = %s;"
        fetched_question = cur.execute(fetch_question, [questionid])
        que_result = cur.fetchall()

        for i in que_result:
            final_result.append(dict(question_id=questionid, no_of_answers=no_of_answers,
                                    question_title=i[2], question_description=i[3]))

        return final_result


        

