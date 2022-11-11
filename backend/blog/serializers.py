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
		t = timezone.now() - releaseTime
		if timezone.timedelta(hours=1) <= t < timezone.timedelta(days=1):
			data['releaseTime'] = str(t.seconds // 3600) + "小时前"
		elif timezone.timedelta(minutes=1) < t < timezone.timedelta(hours=1):
			data['releaseTime'] = str(t.seconds // 60) + "分钟前"
		else:
			data['releaseTime'] = releaseTime.strftime('%Y-%m-%d')
		data['authorName'] = instance.authorName.username
		return data
		