import base64
import os

from django.utils import timezone
from rest_framework import serializers
from .models import Merchandise
from backend.settings import WEB_HOST_MEDIA_URL


class MerchandiseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Merchandise
		fields = '__all__'
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
		# data['image'] = str(base64.b64encode(open(instance.image.path, 'rb').read()), encoding='utf-8')
		urls = os.path.join(WEB_HOST_MEDIA_URL, str(instance.image))
		data['image'] = urls
		time = instance.time
		# change the format of time
		t = timezone.now() - time
		if timezone.timedelta(hours=1) <= t < timezone.timedelta(days=1):
			data['time'] = str(t.seconds // 3600) + " hours ago"
		elif timezone.timedelta(minutes=1) < t < timezone.timedelta(hours=1):
			data['time'] = str(t.seconds // 60) + " minutes ago"
		elif timezone.timedelta(minutes=1) >= t:
			data['time'] = "just now"
		else:
			data['time'] = time.strftime('%Y-%m-%d')
		data['originalTime'] = instance.time  # to compare the time
		data['username'] = instance.username.username
		return data
