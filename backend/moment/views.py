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
def sendMoment(request):
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
		