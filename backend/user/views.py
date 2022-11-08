from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import JsonResponse

# Create your views here.


from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import User, Follow


# sign up
# return {'code': number}
# number:
# 0 --> success
# 1 --> username has already existed
# 2 --> request method is not POST
# 3 --> user who has logged in cannot sign up
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
# return {'code': number}
# number:
# 0 --> success
# 1 --> username or password is wrong
# 2 --> request method is not POST
# 3 --> user who has entered can't log in again
@csrf_exempt
def login(request):
	if request.method == 'POST':
		if request.user.is_authenticated:
			return JsonResponse({'code': 3}, status=status.HTTP_200_OK)
		
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
		else:
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
	return JsonResponse({'code': 2}, status=status.HTTP_400_BAD_REQUEST)


# logout
# return {'code': number}
# number:
# 0 --> success
# 1 --> user who has not logged in cannot log out
# GET method
def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
	return JsonResponse({'code': 1}, status=status.HTTP_200_OK)


# follow
# return {'code': number}
# number:
# 0 --> success follow
# 1 --> cancel follow
# 2 --> request method is not POST
# 3 --> visitor needs to log in
# 4 --> user cannot follow himself
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
