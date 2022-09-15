import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import db


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def get_question(request) -> HttpResponse:
    if request.method == 'GET':
        return HttpResponse(db.get_question(), content_type='application/json')
    return HttpResponse(status=503)


def get_history(request) -> HttpResponse:
    if request.method == 'GET':
        return HttpResponse(db.get_history(), content_type='application/json')
    return HttpResponse(status=503)


def get_user(request) -> HttpResponse:
    if request.method == 'GET':
        return HttpResponse(db.get_user(), content_type='application/json')
    return HttpResponse(status=503)


@csrf_exempt
def delete_history(request, table_id: int) -> HttpResponse:
    if request.method == 'DELETE':
        db.delete_history(table_id)
        return HttpResponse(status=200)
    return HttpResponse(status=503)


@csrf_exempt
def add_question(request) -> HttpResponse:
    if request.method == 'PUT':
        db.add_question(json.dumps(request.body, ensure_ascii=False, cls=BytesEncoder))
        return HttpResponse(status=200)
    return HttpResponse(status=503)


@csrf_exempt
def add_user(request) -> HttpResponse:
    if request.method == 'PUT':
        db.add_user(json.dumps(request.body, ensure_ascii=False, cls=BytesEncoder))
        return HttpResponse(status=200)
    return HttpResponse(status=503)


def search_history(request) -> HttpResponse:
    if request.method == 'GET':
        history_json = db.search_history(request.GET.get('search', default=None))
        return HttpResponse(history_json, content_type='application/json')
    return HttpResponse(status=503)


@csrf_exempt
def change_answer(request, question_id: int) -> HttpResponse:
    if request.method == 'POST':
        db.change_answer(question_id, [x for x in request.POST.get('answer', default='')])
        return HttpResponse(status=200)
    return HttpResponse(status=503)
