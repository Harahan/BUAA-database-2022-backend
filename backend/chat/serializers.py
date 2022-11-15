import os

from django.utils import timezone
from rest_framework import serializers
from .models import Chat, Record
from backend.settings import WEB_HOST_MEDIA_URL


class ChatSerializer(serializers.ModelSerializer):
	class Meta:
		model = Chat
		fields = ('id', 'name', 'owner', 'time', 'type', 'avatar')
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
		data['owner'] = instance.owner.username
		time = instance.time
		data['avatar'] = os.path.join(WEB_HOST_MEDIA_URL, str(instance.avatar))
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
		if instance.record_set.exists():
			latest = instance.record_set.order_by('-time').first()
			data['latest'] = dict(RecordSerializer(latest).data)
		else:
			data['latest'] = dict()
		return data


class RecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = Record
		fields = ('time', 'content')
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
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
		data['username'] = instance.user.username
		data['avatar'] = os.path.join(WEB_HOST_MEDIA_URL, str(instance.user.avatar))
		data['content'] = instance.content
		data['originalTime'] = instance.time  # to compare the time
		return data
