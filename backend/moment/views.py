# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from user.models import User, Follow
# Create your views here.
from .models import Moment
from .serializers import MomentSerializer


def sendMoment(request):
	if request.method == 'GET':
		if not request.user.is_authenticated:
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
		user = request.user
		users = [user]
		if Follow.objects.filter(follower=user).exists():
			users += Follow.objects.filter(follower=user).values_list('followee', flat=True)
		rt = []
		for u in users:
			user_filter = Moment.objects.filter(user=u)
			if user_filter.exists():
				# print(user_filter)
				# print(MomentSerializer(user_filter, many=True).data)
				rt += list(MomentSerializer(user_filter, many=True).data)
		rt.sort(key=lambda x: x['originalTime'], reverse=True)
		return JsonResponse({'code': 0, 'data': rt}, status=status.HTTP_200_OK)
		