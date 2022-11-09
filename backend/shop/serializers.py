import base64

from rest_framework import serializers
from .models import Merchandise


class MerchandiseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Merchandise
		fields = '__all__'
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
		data['image'] = str(base64.b64encode(open(instance.image.path, 'rb').read()), encoding='utf-8')
		return data
