from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from user.models import User
from .models import Article
from .serializers import ArticleSerializer
# Create your views here.


# fetch all articles
# 404 if request method is not GET
# the domains of image and userPhoto are not exist


def fetchAll(request):
	if request.method == 'GET':
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles, many=True, allow_null=True)
		return JsonResponse(serializer.data, safe=False)
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
def fetchOne(request):
	if request.method == 'GET':
		article = Article.objects.filter(authorName=User.objects.get(username=request.GET.get('author_Name')),
										 title=request.GET.get('tit'))
		serializer = ArticleSerializer(article, many=True)  # may be not only one article
		return JsonResponse(serializer.data, safe=False)
	return HttpResponse(status=status.HTTP_404_NOT_FOUND)
	
	
	