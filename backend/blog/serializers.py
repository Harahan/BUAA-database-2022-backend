import os

from django.utils import timezone
from rest_framework import serializers
from selectolax.parser import HTMLParser

from . import models
from .models import AreaWithArticle
from backend.settings import WEB_HOST_MEDIA_URL


class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Article
		fields = '__all__'
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
		releaseTime = instance.releaseTime
		# change the format of releaseTime
		t = timezone.now() - releaseTime
		if timezone.timedelta(hours=1) <= t < timezone.timedelta(days=1):
			data['releaseTime'] = str(t.seconds // 3600) + " hours ago"
		elif timezone.timedelta(minutes=1) < t < timezone.timedelta(hours=1):
			data['releaseTime'] = str(t.seconds // 60) + " minutes ago"
		elif timezone.timedelta(minutes=1) >= t:
			data['releaseTime'] = "just now"
		else:
			data['releaseTime'] = releaseTime.strftime('%Y-%m-%d')
		data['originalTime'] = instance.releaseTime  # to compare the time
		data['authorName'] = instance.authorName.username
		data['categories'] = []
		if AreaWithArticle.objects.filter(article=instance).exists():
			data['categories'] = [a.area.areaName for a in AreaWithArticle.objects.filter(article=instance)]
		data['userPhoto'] = os.path.join(WEB_HOST_MEDIA_URL, str(instance.authorName.avatar))
		file = open(instance.html.path, 'r', encoding='utf-8').read()
		data['digest'] = HTMLParser(file).text().replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
		data['html'] = os.path.join(WEB_HOST_MEDIA_URL, str(instance.html))
		data['cover'] = os.path.join(WEB_HOST_MEDIA_URL, str(instance.cover))
		if str(instance.cover).endswith("default.jpg"):
			data['cover'] = ""
		return data
		