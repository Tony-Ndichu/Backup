def get_answers(**kwargs):

	user_details=[]
	answer_list = []

	if kwargs is not None:
		for questionid, value in kwargs.iteritems():
			dict(%s == %s % ( questionid, value ) )

		fetch_user_answers = "SELECT * FROM answers WHERE question_id = %s;"
        fetched_answers = cur.execute(fetch_user_answers, [value])
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
        answer_list.append(dict(answer_id=i[0], user_id=i[
            1], question_id=i[2], answer_body=i[3], accepted=i[4]))

    return answer_list