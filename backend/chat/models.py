from django.db import models


# Create your models here.
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver


class Chat(models.Model):
	TYPE = (
		('group', 'group'),
		('private', 'private'),
	)
	
	name = models.CharField(max_length=100, default='')
	# description = models.CharField(max_length=200)
	member = models.ManyToManyField('user.User', related_name='chat_member', blank=True)
	owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='chat_owner')
	time = models.DateTimeField(auto_now_add=True)
	type = models.CharField(max_length=10, choices=TYPE)
	avatar = models.ImageField(upload_to='group', default='chat/default.jpg')
		
	def __str__(self):
		return self.name


class Record(models.Model):
	chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	content = models.TextField()
	time = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		unique_together = ('chat', 'user', 'time')
