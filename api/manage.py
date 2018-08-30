from .database.connect import conn, cur
import psycopg2

def tables(value):

    if value == "create":
        """ 
        create tables in the database
        """
        create_users = """ CREATE TABLE IF NOT EXISTS users (
              id bigserial NOT NULL PRIMARY KEY,
              first_name varchar(155) NOT NULL,
              last_name varchar(255) NOT NULL,
              username varchar(255) UNIQUE NOT NULL,
              email varchar(255) UNIQUE NOT NULL,
              password varchar(255) NOT NULL
            )
            """
        

        create_questions = """ CREATE TABLE IF NOT EXISTS questions (
                id bigserial NOT NULL PRIMARY KEY,
                user_id int NOT NULL,
                title varchar(100) UNIQUE NOT NULL,
                description varchar(255) NOT NULL 
            )
            """

        create_answers = """CREATE TABLE IF NOT EXISTS answers (
                id bigserial NOT NULL PRIMARY KEY,
                user_id int NOT NULL,
                question_id int NOT NULL,
                answer_body varchar(255) UNIQUE NOT NULL,
                accepted varchar(255)
            )
            """

        create_comments = """CREATE TABLE IF NOT EXISTS comments (
                id bigserial NOT NULL PRIMARY KEY,
                user_id int NOT NULL,
                answer_id int NOT NULL,
                comment_body varchar(255) UNIQUE NOT NULL
            )
            """

        create_token = """CREATE TABLE IF NOT EXISTS tokens (
                id bigserial NOT NULL PRIMARY KEY,
                jti varchar(255) NOT NULL
            )
            """



        table_list= [create_users , create_questions , create_answers, create_token, create_comments ]

    elif value == "drop":
        """ 
        drop tables in the database
        """
        drop_users = "DROP TABLE IF EXISTS users"

        drop_questions = "DROP TABLE IF EXISTS questions"

        drop_answers = "DROP TABLE IF EXISTS answers"

        drop_comments = "DROP TABLE IF EXISTS comments"

        drop_token = "DROP TABLE IF EXISTS token"

        table_list= [drop_users , drop_questions , drop_answers, drop_token, drop_comments ]
            
    try:
        # create table one by one
        for table in table_list:
            cur.execute(table)
        # close communication with the PostgreSQL database server
        
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
