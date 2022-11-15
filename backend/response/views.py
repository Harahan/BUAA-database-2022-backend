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
		obj_id = request.POST.get('obj_id')
		obj_type = request.POST.get('obj_type')
		

	
@csrf_exempt
def add_or_cancel_like(request):
	if request.method == 'POST':
		obj_id = request.POST.get('obj_id')
		obj_type = request.POST.get('obj_type')
		username = request.POST.get('username')
		user = User.objects.get(username=username)
		
	

@csrf_exempt
def add_or_cancel_dislike(request):
	if request.method == 'POST':
		pass
	
	
@csrf_exempt
def del_comment(request):
	if request.method == 'POST':
		pass
	