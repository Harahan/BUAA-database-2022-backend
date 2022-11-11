import base64
import os

from backend.settings import WEB_HOST_MEDIA_URL
from django.utils import timezone
from rest_framework import serializers
from .models import User, Follow
# import os


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'avatar', 'date_joined')
		
	def to_representation(self, instance):
		data = super().to_representation(instance)
		date_joined = instance.date_joined
		# change the format of releaseTime
		# print(date_joined - timezone.now())
		t = timezone.now() - date_joined
		if timezone.timedelta(hours=1) <= t < timezone.timedelta(days=1):
			data['date_joined'] = str(t.seconds // 3600) + "小时前"
		elif timezone.timedelta(minutes=1) < t < timezone.timedelta(hours=1):
			data['date_joined'] = str(t.seconds // 60) + "分钟前"
		else:
			data['date_joined'] = date_joined.strftime('%Y-%m-%d')
		data['code'] = 0
		urls = os.path.join(WEB_HOST_MEDIA_URL, str(instance.avatar))
		data['avatar'] = urls
		return data
		
		