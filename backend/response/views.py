from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from .models import Comment, Like, Dislike
from user.models import User


@csrf_exempt
def add_comment(request):
	if request.method == 'POST':
		pass
	
	
@csrf_exempt
def add_like(request):
	if request.method == 'POST':
		pass
	

@csrf_exempt
def add_dislike(request):
	if request.method == 'POST':
		pass
	