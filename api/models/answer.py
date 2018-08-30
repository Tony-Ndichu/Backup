"""

#app/api/models/answer.py
This is the answer model
"""
from datetime import datetime
from ..database.connect import conn, cur


class AnswerModel():
    """handles operations for the answers"""

    def __init__(self, answer):
        self.answer = answer
        self.answer_date = datetime.now()

    def get_answers(*args):

        user_details=[]
        answer_list = []

        if args is not None:
            for questionid in args:
                fetch_user_answers = "SELECT * FROM answers WHERE question_id = %s;"
                fetched_answers = cur.execute(fetch_user_answers, [questionid])
                result = cur.fetchall()


        que = cur.execute("SELECT * FROM answers")

        try:
            que
        except (Exception, psycopg2.DatabaseError) as error:
            print (error)
            conn
            cur

        result = cur.fetchall()


        for i in result:
            answer_list.append(i)

        return answer_list


    def save_answer(res):
        """save new answer"""

        submit = cur.execute("""INSERT INTO answers(user_id, question_id, answer_body, accepted ) VALUES 
                    (%(arg1)s, %(arg2)s, %(arg3)s, false )""", res)

        conn.commit()

        return "Successfully added answer"

    def check_if_already_accepted(answer_id):
        """check if user already accepted the answers"""

        fetch_question = "SELECT * FROM answers WHERE id = %s;"
        fetched_question = cur.execute(fetch_question, [answer_id])
        result = cur.fetchall()

        for i in result:
            if i[4] == 'true':
                return "You have already accepted this answer"

    def accept_answer(answer_id):
        """accepts and answeer"""

        update_que = "UPDATE answers SET accepted = true WHERE id = %s;"
        cur.execute(update_que, [answer_id])
        conn.commit()

        return "Successfully accepted answer"

