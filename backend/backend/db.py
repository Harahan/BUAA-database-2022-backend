import json
import sqlite3

conn = sqlite3.connect('../proj1.db')
cursor = conn.cursor()


def get_question() -> json:
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
    def tuple2dict(x):
        return {
            "highest_score": x[0],
            "name": x[1],
            "password": x[2]
        }

    sql = """select 
                answer, history_type, practice_time, question_id, score, table_id
            from 
                history_bank"""
    cursor.execute(sql)
    total = cursor.fetchall()
    result = map(tuple2dict, total)
    return json.dumps(list(result))

def delete_history(question_id: int) -> None:
    pass


def add_question(question: json) -> None:
    pass


def add_user(user: json) -> None:
    pass


def search_history(key_words: str) -> json:
    return json.dumps([
        {
            "answer": "",
            "history_type": "搜索题目",
            "practice_time": 0,
            "question_id": 98,
            "score": -1.0,
            "table_id": 1
        },
    ])


def change_answer(question_id: int, answer: []) -> None:
    pass
