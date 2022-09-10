import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import db


def get_question(request) -> json:
	if request.method == 'GET':
		return HttpResponse(db.get_question(), content_type='application/json')


def get_history(request) -> json:
	if request.method == 'GET':
		return HttpResponse(db.get_history(), content_type='application/json')


def get_user(request) -> json:
	if request.method == 'GET':
		return HttpResponse(db.get_user(), content_type='application/json')


@csrf_exempt
def delete_history(request, question_id: int) -> None:
	if request.method == 'DELETE':
		db.delete_history(question_id)


@csrf_exempt
def add_question(request) -> None:
	if request.method == 'PUT':
		db.add_question(json.dumps(request.body))


@csrf_exempt
def add_user(request) -> None:
	if request.method == 'PUT':
		db.add_user(json.dumps(request.body))


def search_history(request) -> json:
	if request.method == 'GET':
		history_json = db.search_history(request.GET.get('search', default=None))
		return HttpResponse(history_json, content_type='application/json')


@csrf_exempt
def change_answer(request, question_id: int) -> None:
	if request.method == 'POST':
		db.change_answer(question_id, [x for x in request.POST.get('ans', default='')])
