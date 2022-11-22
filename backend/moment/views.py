# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from user.models import User, Follow
from response.models import Like, Dislike, Comment
# Create your views here.
from .models import Moment
from .serializers import MomentSerializer


@csrf_exempt
def send_moment(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
		rt = []
		user = request.user
		users = [user]
		if Follow.objects.filter(follower=user).exists():
			users += Follow.objects.filter(follower=user).values_list('followee', flat=True)
		for u in users:
			user_filter = Moment.objects.filter(user=u)
			if user_filter.exists():
				# print(user_filter)
				# print(MomentSerializer(user_filter, many=True).data)
				rt += list(MomentSerializer(user_filter, many=True).data)
		if request.POST.get('content'):
			content = request.POST.get('content')
			user = request.user
			moment = Moment.objects.create(content=content, user=user)
			rt.append(MomentSerializer(moment).data)
		rt.sort(key=lambda x: x['originalTime'], reverse=True)
		for data in rt:
			moment_id = data['id']
			username = request.user.username
			if Like.objects.filter(obj_id=moment_id, user__username=username, obj_type=0).exists():
				data['stance'] = 1
			elif Dislike.objects.filter(obj_id=moment_id, user__username=username, obj_type=0).exists():
				data['stance'] = -1
			else:
				data['stance'] = 0
		return JsonResponse({'code': 0, 'data': rt}, status=status.HTTP_200_OK)
		
		
@csrf_exempt
def get_moment(request):
	if request.method == 'POST':
		moment_id = request.POST.get('id')
		if Moment.objects.filter(id=moment_id).exists():
			moment = Moment.objects.get(id=moment_id)
			serializer = dict(MomentSerializer(moment).data)
			username = request.user.username
			if Like.objects.filter(obj_id=moment_id, user__username=username, obj_type=0).exists():
				serializer['stance'] = 1
			elif Dislike.objects.filter(obj_id=moment_id, user__username=username, obj_type=0).exists():
				serializer['stance'] = -1
			else:
				serializer['stance'] = 0
			return JsonResponse(serializer, status=status.HTTP_200_OK)
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)
	return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def del_moment(request):
	if request.method == 'POST':
		moment_id = request.POST.get('id')
		if not request.user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		if Moment.objects.filter(id=moment_id).exists():
			user = request.user
			moment = Moment.objects.get(id=moment_id)
			if moment.user == user:
				moment.delete()
				return HttpResponse(status=status.HTTP_200_OK)
			else:
				return HttpResponse(status=status.HTTP_403_FORBIDDEN)
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)
	return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
