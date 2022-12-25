import datetime

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

from .serializers import CommentSerializer


@csrf_exempt
def take_stance(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		x = [Moment, Article, Comment, Merchandise, User]
		obj_id = int(request.POST.get('obj_id'))
		obj_type = int(request.POST.get('obj_type'))
		stance = int(request.POST.get('stance'))
		tag = True
		if not x[obj_type].objects.filter(id=obj_id).exists():
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
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
		obj = x[obj_type].objects.get(id=obj_id)
		return JsonResponse({'tot_like': obj.tot_like, 'tot_dislike': obj.tot_dislike}, safe=False)
		
		
@csrf_exempt
def add_comment(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		x = [Moment, Article, Merchandise]
		obj_id = int(request.POST.get('obj_id'))
		obj_type = int(request.POST.get('obj_type'))
		content = request.POST.get('content')
		if not x[obj_type].objects.filter(id=obj_id).exists():
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		comment = Comment(user=request.user, obj_id=obj_id, obj_type=obj_type, content=content, time=datetime.datetime.now())
		comment.save()
		return JsonResponse({"id": comment.id}, status=status.HTTP_200_OK)
	
	
@csrf_exempt
def del_comment(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		comment_id = int(request.POST.get('id'))
		if not Comment.objects.filter(id=comment_id).exists():
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		comment = Comment.objects.get(id=comment_id)
		if comment.user != request.user:
			return HttpResponse(status=status.HTTP_403_FORBIDDEN)
		comment.delete()
		return HttpResponse(status=status.HTTP_200_OK)
	
	
@csrf_exempt
def find_comment(request):
	if request.method == 'POST':
		comment_id = int(request.POST.get('id'))
		if not Comment.objects.filter(id=comment_id).exists():
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		comment = Comment.objects.get(id=comment_id)
		serializer = CommentSerializer(comment)
		return JsonResponse(serializer.data, status=status.HTTP_200_OK)
	
	
@csrf_exempt
def find_comments(request):
	if request.method == 'POST':
		x = [Moment, Article, Merchandise]
		obj_id = int(request.POST.get('obj_id'))
		obj_type = int(request.POST.get('obj_type'))
		if not x[obj_type].objects.filter(id=obj_id).exists():
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		comments = Comment.objects.filter(obj_id=obj_id, obj_type=obj_type)
		serializer = CommentSerializer(comments, many=True)
		serializer_data = serializer.data
		for data in serializer_data:
			if request.user.is_authenticated:
				if Like.objects.filter(user=request.user, obj_id=data['id'], obj_type=2).exists():
					data['stance'] = 1
				elif Dislike.objects.filter(user=request.user, obj_id=data['id'], obj_type=2).exists():
					data['stance'] = -1
				else:
					data['stance'] = 0
			else:
				data['stance'] = 0
		rt = serializer.data
		rt = sorted(rt, key=lambda x: x['originalTime'], reverse=True)
		return JsonResponse(rt, safe=False, status=status.HTTP_200_OK)
	