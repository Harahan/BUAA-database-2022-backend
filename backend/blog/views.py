import os.path
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from selectolax.parser import HTMLParser
from user.models import User
from .models import Article, Area, AreaWithArticle
from .serializers import ArticleSerializer
from backend.settings import WEB_HOST_MEDIA_URL, MEDIA_ROOT
# Create your views here.


# fetch all articles
# 404 if request method is not GET
# the domains of image and userPhoto are not exist


def fetch_all(request):
	if request.method == 'GET':
		articles = Article.objects.all()
		if articles:
			serializer = ArticleSerializer(articles, many=True, allow_null=True)
			return JsonResponse(serializer.data, safe=False)
		else:
			return JsonResponse({}, safe=False)
	return HttpResponse(status=status.HTTP_404_NOT_FOUND)
	

# delete an article
# return {'code': number}
# number:
# 0 --> success
# 1 --> article doesn't exist
# 2 --> request method is not POST
# 3 --> the user is not the author of the article or the user is not admin or the user has not logged in
# ----------- there is no admin user now -----------
@csrf_exempt
def delete(request):
	if request.method == 'POST':
		article = Article.objects.filter(authorName=User.objects.get(username=request.POST['username']),
									  title=request.POST['tit'])
		if article and article[0].authorName.username == request.POST['username']:
			article.delete()
			return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
		elif article:
			return JsonResponse({'code': 3}, status=status.HTTP_200_OK)
		elif article and article[0].authorName != request.POST['username']:
			return JsonResponse({'code': 3}, status=status.HTTP_200_OK)
		else:
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
	return JsonResponse({'code': 2}, status=status.HTTP_400_BAD_REQUEST)


# fetch an article
# 404 if request method is not GET
# the domains of image and userPhoto are not exist
def fetch_one(request):
	if request.method == 'GET':
		if User.objects.filter(username=request.GET['author_Name']).exists():
			article = Article.objects.filter(authorName=User.objects.get(username=request.GET.get('author_Name')),
											 title=request.GET.get('tit'))
			# print("ddd")
			if article:
				serializer = ArticleSerializer(article, many=True)  # may be not only one article
				return JsonResponse(serializer.data, safe=False)
			else:
				return JsonResponse({}, safe=False)
	return HttpResponse(status=status.HTTP_404_NOT_FOUND)
	
	
# upload a picture
@csrf_exempt
def upload_picture(request):
	if request.method == 'POST':
		try:
			picture = request.FILES.get('picture')
			name = get_random_str() + ".jpg"
			filepath = MEDIA_ROOT / "article/picture" / name
			with open(filepath, 'wb') as f:
				for info in picture.chunks():
					f.write(info)
		except Exception:
			return JsonResponse({'code': 1, 'url': ""}, status=status.HTTP_200_OK)
		return JsonResponse({'code': 0, 'url': os.path.join(WEB_HOST_MEDIA_URL, "article/picture/" + name)}, status=status.HTTP_200_OK)
	
	
def get_random_str(length=10):
	s = ''
	chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
	l = len(chars) - 1
	for i in range(length):
		s += chars[random.randint(0, l)]
	return s


# upload an article
@csrf_exempt
def post_article(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return JsonResponse({'code': 1}, status=status.HTTP_200_OK)
		user = request.user
		if Article.objects.filter(authorName=user, title=request.POST['title']).exists():
			return JsonResponse({'code': 2}, status=status.HTTP_200_OK)
		if request.POST['cover'] == "":
			Article.objects.create(authorName=user,
								   title=request.POST['title'],
								   html=request.FILES.get('html'))
		else:
			Article.objects.create(authorName=user,
								   title=request.POST['title'],
								   html=request.FILES.get('html'),
								   cover=request.POST['cover'])
		tags = request.POST['tags'].split(',')
		for tag in tags:
			if not Area.objects.filter(areaName=tag).exists():
				Area.objects.create(areaName=tag)
			area = Area.objects.get(areaName=tag)
			article = Article.objects.get(title=request.POST['title'], authorName=user)
			if not AreaWithArticle.objects.filter(area=area, article=article).exists():
				AreaWithArticle.objects.create(article=article, area=area)
		return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
			