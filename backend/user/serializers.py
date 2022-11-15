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
		fields = ('id', 'username', 'email', 'avatar', 'date_joined', 'tot_like', 'tot_dislike')
		
	def to_representation(self, instance):
		data = super().to_representation(instance)
		date_joined = instance.date_joined
		# change the format of releaseTime
		# print(date_joined - timezone.now())
		t = timezone.now() - date_joined
		if timezone.timedelta(hours=1) <= t < timezone.timedelta(days=1):
			data['date_joined'] = str(t.seconds // 3600) + " hours ago"
		elif timezone.timedelta(minutes=1) < t < timezone.timedelta(hours=1):
			data['date_joined'] = str(t.seconds // 60) + " minutes ago"
		elif timezone.timedelta(minutes=1) >= t:
			data['date_joined'] = "just now"
		else:
			data['date_joined'] = date_joined.strftime('%Y-%m-%d')
		data['originalDateJoined'] = instance.date_joined  # to compare the time
		data['code'] = 0
		urls = os.path.join(WEB_HOST_MEDIA_URL, str(instance.avatar))
		data['avatar'] = urls
		return data
		
		