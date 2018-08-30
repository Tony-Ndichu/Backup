import psycopg2
import os


if os.getenv('CONFIG') == 'development':
	conn_string = os.getenv("DB_URL")
elif os.getenv('CONFIG') == 'testing':
	conn_string = os.getenv("DB_TEST_URL")

conn = psycopg2.connect(conn_string)
cur = conn.cursor()