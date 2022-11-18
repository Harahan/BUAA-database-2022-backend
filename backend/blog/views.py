import os.path
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from selectolax.parser import HTMLParser
from user.models import User, Follow
from .models import Article, Area, AreaWithArticle
from .serializers import ArticleSerializer
from backend.settings import WEB_HOST_MEDIA_URL, MEDIA_ROOT
from fuzzywuzzy import fuzz
from PIL import Image
import os
# Create your views here.


def fetch_all(request):
	if request.method == 'GET':
		articles = Article.objects.all()
		if not articles:
			return JsonResponse([], safe=False)
		if request.GET['follow'] == 'true':
			if not request.user.is_authenticated:
				return JsonResponse([], status=status.HTTP_200_OK)
			if Follow.objects.filter(follower=request.user).exists():
				articles1 = articles.filter(authorName_id__in=
										   Follow.objects.filter(follower=request.user).values_list('followee', flat=True))
				articles = articles.filter(authorName=request.user) | articles1
				if not articles:
					return JsonResponse([], safe=False)
			else:
				articles = articles.filter(authorName=request.user)
				if not articles:
					return JsonResponse([], safe=False)
		if request.GET['tag']:
			tag_list = request.GET['tag'].split(',')
			if Area.objects.filter(areaName__in=tag_list).exists():
				# 作为外码存的是id
				articles2 = None
				for tag in tag_list:
					tmp_articles = AreaWithArticle.objects.filter(area__areaName=tag).values_list('article', flat=True)
					if articles2:
						articles2 = articles2.intersection(tmp_articles)
					elif tmp_articles:
						articles2 = tmp_articles
				if articles2 is not None:
					articles = articles.filter(id__in=articles2)
					if not articles:
						return JsonResponse([], safe=False)
				else:
					return JsonResponse([], safe=False)
			else:
				return JsonResponse([], safe=False)
		if request.GET['search']:
			title = request.GET['search']
			articles3 = []
			for article in articles:
				if fuzz.ratio(article.title, title) > 30:
					articles3.append(article)
			if articles3:
				articles = articles3
			else:
				return JsonResponse([], safe=False)
		serializer = ArticleSerializer(articles, many=True)
		# serializer.data.sort(key=lambda x: x['releaseTime'], reverse=True)
		serializer_data = sorted(serializer.data, key=lambda x: x['originalTime'], reverse=True)
		return JsonResponse(serializer_data, safe=False)
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
@csrf_exempt
def fetch_one(request):
	if request.method == 'POST':
		if User.objects.filter(username=request.POST.get('author_Name')).exists():
			article = Article.objects.filter(authorName=User.objects.get(username=request.POST.get('author_Name')),
											 title=request.POST.get('tit'))
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
			cover = request.POST['cover'].split('/')[-1]
			Article.objects.create(authorName=user,
								   title=request.POST['title'],
								   html=request.FILES.get('html'),
								   cover='article/picture/' + cover)
		tags = request.POST['tags'].split(',')
		for tag in tags:
			if not Area.objects.filter(areaName=tag).exists():
				Area.objects.create(areaName=tag)
			area = Area.objects.get(areaName=tag)
			article = Article.objects.get(title=request.POST['title'], authorName=user)
			if not AreaWithArticle.objects.filter(area=area, article=article).exists():
				AreaWithArticle.objects.create(article=article, area=area)
		return JsonResponse({'code': 0}, status=status.HTTP_200_OK)
	
	
# fetch articles for the user
@csrf_exempt
def fetch_user_articles(request):
	if request.method == 'POST':
		if not User.objects.filter(username=request.POST['username']).exists():
			return JsonResponse([], safe=False)
		user = User.objects.get(username=request.POST.get('username'))
		# print(user.is_authenticated)
		articles = Article.objects.filter(authorName=user)
		if not articles:
			return JsonResponse([], safe=False)
		serializer = ArticleSerializer(articles, many=True)
		op = request.POST['op']
		serializer_data = sorted(serializer.data, key=lambda x: x['originalTime'], reverse=True if int(op) == 0 else False)
		return JsonResponse(serializer_data, safe=False)
	