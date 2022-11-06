from django.utils import timezone
from rest_framework import serializers
from . import models


class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Article
		fields = '__all__'
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
		releaseTime = instance.releaseTime
		# change the format of releaseTime
		if timezone.timedelta(hours=1) <= releaseTime - timezone.now() < timezone.timedelta(days=1):
			data['releaseTime'] = (releaseTime - timezone.now()).hours + "小时前"
		elif releaseTime - timezone.now() < timezone.timedelta(hours=1):
			data['releaseTime'] = (releaseTime - timezone.now()).minutes + "分钟前"
		else:
			data['releaseTime'] = releaseTime.strftime('%Y-%m-%d')
		data['authorName'] = instance.authorName.username
		return data
		