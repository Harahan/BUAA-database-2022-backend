import os.path

from django.db import models
from django.utils import timezone
from backend.settings import MEDIA_ROOT, WEB_HOST_MEDIA_URL
from django.db.models.signals import pre_delete
# from response.models import Comment, Like, Dislike
from django.dispatch import receiver

from selectolax.parser import HTMLParser

# Create your models here.


class Article(models.Model):
	authorName = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)  # the authorName is an instance of User
	releaseTime = models.DateTimeField(auto_now=True)
	# categories = models.CharField(max_length=1024)
	title = models.CharField(max_length=120)
	# digest = models.TextField()  # actually this is the article's content
	html = models.FileField(upload_to='article/html', default='article/html/default.html')
	cover = models.ImageField(upload_to='article/picture', default='article/picture/default.jpg')
	tot_like = models.IntegerField(default=0)
	tot_comment = models.IntegerField(default=0)
	tot_dislike = models.IntegerField(default=0)

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
	
	
# del like, dislike, comment before del article
@receiver(pre_delete, sender=Article)
def del_like_dislike_comment(sender, instance, **kwargs):
	from response.models import Comment, Like, Dislike
	article_id = instance.id
	Like.objects.filter(obj_type=1, obj_id=article_id).delete()
	Dislike.objects.filter(obj_type=1, obj_id=article_id).delete()
	Comment.objects.filter(obj_type=1, obj_id=article_id).delete()
	
	
# del html, cover before del article
# if not the default html, cover, and  not used by other article, delete them
@receiver(pre_delete, sender=Article)
def del_html_cover(sender, instance, **kwargs):
	html_path = os.path.join(MEDIA_ROOT, instance.html.name)
	cover_path = os.path.join(MEDIA_ROOT, instance.cover.name)
	
	if instance.html.name != 'article/html/default.html':
		article_num = Article.objects.filter(html=instance.html).count()
		if article_num == 1:
			os.remove(html_path)
	
	if instance.cover.name != 'article/picture/default.jpg':
		article_num = Article.objects.filter(cover=instance.cover).count()
		if article_num == 1:
			os.remove(cover_path)