import base64
import os

from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import JsonResponse

# Create your views here.

from backend.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import User, Follow
# import settings
from .serializers import UserSerializer


# signup
@csrf_exempt
def signup(request):
	if request.method == 'POST':
		if request.user.is_authenticated:
			return JsonResponse({'code': 3}, status=status.HTTP_200_OK)
		username = request.POST.get('username')
		password = request.POST.get('password')
		if User.objects.filter(username=username).exists():
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
		else:
			user = User.objects.create_user(username=username, password=password)
			user.save()
			return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
		
	return JsonResponse({'code': 2}, status=status.HTTP_400_BAD_REQUEST)


# login
@csrf_exempt
def login(request):
	if request.method == 'POST':
		if request.user.is_authenticated:
			# print(request.user)
			return JsonResponse({'code': 3}, status=status.HTTP_200_OK)
		
		username = request.POST.get('username')
		password = request.POST.get('password')
		# print(username, password)
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth.login(request, user)
			user = User.objects.get(username=username)
			serializer = UserSerializer(user)
			serializer.data['code'] = 0
			return JsonResponse(serializer.data, status=status.HTTP_200_OK)
		else:
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
	return JsonResponse({'code': 2}, status=status.HTTP_400_BAD_REQUEST)


# logout
def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
	return JsonResponse({'code': 1}, status=status.HTTP_200_OK)


# follow
@csrf_exempt
def follow(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return JsonResponse({'code': 3}, status=status.HTTP_200_OK)
		if request.user.username == request.POST.get('authorName'):
			return JsonResponse({'code': 4}, status=status.HTTP_200_OK)
		follower = request.user
		followee = User.objects.get(username=request.POST.get('authorName'))
		if Follow.objects.filter(follower=follower, followee=followee).exists():
			Follow.objects.get(follower=follower, followee=followee).delete()
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
		else:
			Follow.objects.create(followee=followee, follower=follower)
			return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
	return JsonResponse({'code': 2}, status=status.HTTP_400_BAD_REQUEST)


# fix profile
@csrf_exempt
def fix_profile(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return JsonResponse({'code': 3}, status=status.HTTP_200_OK)
		user = request.user
		if request.POST.get('question') and request.POST.get('answer'):
			user.question = request.POST.get('question')
			user.answer = request.POST.get('answer')
		if request.POST.get('email'):
			user.email = request.POST.get('email')
		if request.POST.get('username'):
			if User.objects.filter(username=request.POST.get('username')).exists():
				return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
			user.username = request.POST.get('username')
		if request.POST.get('password'):
			user.set_password(request.POST.get('password'))
		if request.FILES.get('avatar'):
			try:
				user.avatar = request.FILES.get('avatar')
			except Exception:
				return JsonResponse({'code': 4}, status=status.HTTP_200_OK)
		user.save()
		auth.login(request, user)
		return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
	return JsonResponse({'code': 2}, status=status.HTTP_400_BAD_REQUEST)


def get_profile(request):
	if request.method == 'GET':
		if not request.user.is_authenticated:
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
		user = request.user
		serializer = UserSerializer(user)
		serializer.data['code'] = 0
		return JsonResponse(serializer.data, status=status.HTTP_200_OK)