import base64
import os

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
		return data
