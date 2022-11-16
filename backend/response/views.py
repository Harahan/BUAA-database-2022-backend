from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Comment, Like, Dislike
from user.models import User
from moment.models import Moment
from blog.models import Article
from shop.models import Merchandise


@csrf_exempt
def take_stance(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		obj_id = int(request.POST.get('obj_id'))
		obj_type = int(request.POST.get('obj_type'))
		stance = int(request.POST.get('stance'))
		tag = True
		if Like.objects.filter(user=request.user, obj_id=obj_id, obj_type=obj_type).exists():
			if stance != 1:
				like = Like.objects.get(user=request.user, obj_id=obj_id, obj_type=obj_type)
				like.delete()
			else:
				tag = False
		elif Dislike.objects.filter(user=request.user, obj_id=obj_id, obj_type=obj_type).exists():
			if stance != -1:
				dislike = Dislike.objects.get(user=request.user, obj_id=obj_id, obj_type=obj_type)
				dislike.delete()
			else:
				tag = False
		if tag and stance != 0:
			if stance == 1:
				like = Like(user=request.user, obj_id=obj_id, obj_type=obj_type)
				like.save()
			else:
				dislike = Dislike(user=request.user, obj_id=obj_id, obj_type=obj_type)
				dislike.save()
		x = [Moment, Article, Comment, Merchandise, User]
		obj = x[obj_type].objects.get(id=obj_id)
		return JsonResponse({'tot_like': obj.tot_like, 'tot_dislike': obj.tot_dislike}, safe=False)
		