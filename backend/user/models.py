from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
	# email
	# password
	# username
	# date_joined
	# first_name
	# last_name
	avatar = models.ImageField(upload_to='avatar', default='avatar/default.jpg', blank=True)
	question = models.CharField(max_length=1024, default='', blank=True)
	answer = models.CharField(max_length=1024, default='', blank=True)
	tot_like = models.IntegerField(default=0)
	tot_dislike = models.IntegerField(default=0)
	age = models.IntegerField(blank=True, null=True)
	country = models.CharField(max_length=1024, default='', blank=True)

	def __str__(self):
		return self.username
	
	
class Follow(models.Model):
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
	followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')
	
	class Meta:
		unique_together = ('followee', 'follower')  # only one followee can be followed by one follower

	