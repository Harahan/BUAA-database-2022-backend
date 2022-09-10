import json


def get_question() -> json:
	return json.dumps([
		{
			"A": "西昌卫星发射中心",
			"B": "酒泉卫星发射中心",
			"C": "太原卫星发射中心",
			"D": "海南文昌航天发射场",
			"answer": "B",
			"provider": "原始题库",
			"question": "我国载人飞船的发射场为______。\nA.西昌卫星发射中心\nB.酒泉卫星发射中心\nC.太原卫星发射中心\nD.海南文昌航天发射场",
			"question_id": 1,
			"select_question": "我国载人飞船的发射场为______。",
			"type": "客观题"
		},
		{
			"A": "11",
			"B": "15",
			"C": "16",
			"D": "18",
			"answer": "C",
			"provider": "原始题库",
			"question": "国际空间站是人类历史上最庞大的航天工程，共有______个国家参与研制。\nA.11\nB.15\nC.16\nD.18",
			"question_id": 2,
			"select_question": "国际空间站是人类历史上最庞大的航天工程，共有______个国家参与研制。",
			"type": "客观题"
		}
	])


def get_history() -> json:
	return json.dumps([
		{
			"answer": "",
			"history_type": "搜索题目",
			"practice_time": 0,
			"question_id": 98,
			"score": -1.0,
			"table_id": 1
		},
		{
			"answer": "B",
			"history_type": "小练习",
			"practice_time": 1,
			"question_id": 1022,
			"score": 10.0,
			"table_id": 2
		},
		{
			"answer": "B",
			"history_type": "小练习",
			"practice_time": 1,
			"question_id": 213,
			"score": 0.0,
			"table_id": 3
		}
	])


def get_user() -> json:
	return json.dumps([
		{
			"highest_score": 0,
			"name": "hys",
			"password": "123456"
		}
	])


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
