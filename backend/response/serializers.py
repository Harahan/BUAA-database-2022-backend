import os
from backend.settings import WEB_HOST_MEDIA_URL

from django.utils import timezone
from rest_framework import serializers
from .models import Comment, Like, Dislike


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('content', 'tot_like', 'tot_dislike', 'time', 'id')

	def to_representation(self, instance):
		data = super().to_representation(instance)
		data['username'] = instance.user.username
		data['avatar'] = os.path.join(WEB_HOST_MEDIA_URL, str(instance.user.avatar))
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
		return data