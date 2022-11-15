from rest_framework import serializers
from .models import Comment, Like, Dislike


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		# fields = ('user', 'obj_type', 'obj_id', 'content', 'tot_like')

	def to_representation(self, instance):
		data = super().to_representation(instance)
		data['username'] = instance.user.username
		data['avatar'] = instance.user.avatar
		return data