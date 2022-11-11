from django.db import models
from django.utils import timezone


# Create your models here.


class Article(models.Model):
	authorName = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)  # the authorName is an instance of User
	releaseTime = models.DateTimeField(auto_now=True)
	# categories = models.CharField(max_length=1024)
	title = models.CharField(max_length=120)
	digest = models.TextField()  # actually this is the article's content
	
	# ------------- image, userPhoto -------------
	def __str__(self):
		return self.title
	
	
class Area(models.Model):
	areaName = models.CharField(max_length=120)
	
	def __str__(self):
		return self.areaName


class AreaWithArticle(models.Model):
	area = models.ForeignKey('Area', on_delete=models.CASCADE)
	article = models.ForeignKey('Article', on_delete=models.CASCADE)
	
	class Meta:
		unique_together = ('area', 'article')
		