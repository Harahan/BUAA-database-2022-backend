import base64
import os

from django.utils import timezone
from rest_framework import serializers
from .models import Merchandise, COLOR
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
		# data['deliveryTime'] = instance.deliverTime.strftime('%Y-%m-%d')
		# rank, color, status, category
		tot = instance.tot_like + instance.tot_dislike + 2
		data['rank'] = int((instance.tot_like + 1) / tot * 5)
		t = int(instance.color)
		i = 0
		data['color'] = []
		color = list(COLOR.keys())
		while t != 0:
			if (t & 1) == 1:
				data['color'].append(color[i])
				# print(color[i])
			t >>= 1
			i += 1
		# discount status cover the new status
		if instance.price != instance.priceSale:
			data['status'] = 1
		elif timezone.now() - instance.time <= timezone.timedelta(days=1):
			data['status'] = 2
		else:
			data['status'] = 0
		data["color_num"] = instance.color
		return data
