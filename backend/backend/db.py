import json
import sqlite3


def get_question() -> json:
    conn = sqlite3.connect('./proj1.db')
    cursor = conn.cursor()
    def tuple2dict(x):
        return {
            "A": x[0],
            "B": x[1],
            "C": x[2],
            "D": x[3],
            "answer": x[4],
            "provider": x[5],
            "question": x[6],
            "question_id": x[7],
            "select_question": x[8],
            "type": x[9]
        }

    sql = """select
                A, B,C, D, answer, provider, question, question_id, select_question, type
            from
                question_bank"""
    cursor.execute(sql)
    total = cursor.fetchall()
    result = map(tuple2dict, total)
    return json.dumps(list(result))


def get_history() -> json:
    conn = sqlite3.connect('./proj1.db')
    cursor = conn.cursor()
    def tuple2dict(x):
        return {
            "answer": x[0],
            "history_type": x[1],
            "practice_time": x[2],
            "question_id": x[3],
            "score": x[4],
            "table_id": x[5]
        }

    sql = """select
                answer, history_type, practice_time, question_id, score, table_id
            from
                history_bank"""
    cursor.execute(sql)
    total = cursor.fetchall()
    result = map(tuple2dict, total)
    return json.dumps(list(result))


def get_user() -> json:
    conn = sqlite3.connect('./proj1.db')
    cursor = conn.cursor()
    
    def tuple2dict(x):
        return {
            "highest_score": x[0],
            "name": x[1],
            "password": x[2]
        }

    sql = """select
                highest_score, name, password
            from
                user_bank"""
    cursor.execute(sql)
    total = cursor.fetchall()
    result = map(tuple2dict, total)
    return json.dumps(list(result))


def delete_history(table_id: int) -> None:
    conn = sqlite3.connect('./proj1.db')
    cursor = conn.cursor()
    
    sql = f"""delete from
                history_bank
            where
                table_id = {table_id}"""
    cursor.execute(sql)
    conn.commit()
    """
        {
            "A": x[0],
            "B": x[1],
            "C": x[2],
            "D": x[3],
            "answer": x[4],
            "provider": x[5],
            "question": x[6],
            "question_id": x[7],
            "select_question": x[8],
            "type": x[9]
        }
    """


def add_question(question: json) -> None:
    conn = sqlite3.connect('./proj1.db')
    cursor = conn.cursor()
    sql = f"""insert into
                    question_bank
                values
                    ('{question[6]}', '{question[4]}', {question[9]}, {question[8]}, {question[0]},
                    {question[1]}, {question[2]}, {question[3]}, {question[5]}, {question[7]})"""
    cursor.execute(sql)
    conn.commit()
    """
        {
            "highest_score": x[0],
            "name": x[1],
            "password": x[2]
        }
    """


def add_user(user: json) -> None:
    conn = sqlite3.connect('./proj1.db')
    cursor = conn.cursor()
    sql = f"""insert or replace into
                    user_bank
                values
                    ({user[0]}, '{user[1]}', '{user[2]}')"""
    cursor.execute(sql)
    conn.commit()


def search_history(key_words: str) -> json:
    conn = sqlite3.connect('./proj1.db')
    cursor = conn.cursor()
    sql = f"""select
                    h.answer answer, h.history_type history_type, h.practice_time practice_time,
                    h.question_id question_id, h.score score, h.table_id table_id
                from 
                    history_bank h
                join
                    question_bank q
                on
                    h.question_id = q.question_id
                where
                    q.select_question like '%{key_words}%'
                order by
                    question_id
                """
    cursor.execute(sql)
    x = cursor.fetchone()
    if x is not None:
        result = {
            "answer": x[0],
            "history_type": x[1],
            "practice_time": x[2],
            "question_id": x[3],
            "score": x[4],
            "table_id": x[5]
        }
    else:
        result = {
            "answer": "",
            "history_type": "",
            "practice_time": 0,
            "question_id": 0,
            "score": 0,
            "table_id": 0
        }
    return json.dumps(result)


def change_answer(question_id: int, answer: []) -> None:
    conn = sqlite3.connect('./proj1.db')
    cursor = conn.cursor()
    answer.sort()
    sql = f"""update
                    user_bank
                set 
                    answer = '{"-".join(answer)}'
                where
                    question_id = {question_id}"""
    cursor.execute(sql)
    conn.commit()
