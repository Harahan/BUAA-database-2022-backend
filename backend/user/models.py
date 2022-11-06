from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
	pass

	def __str__(self):
		return self.username
	
	
class Follow(models.Model):
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
	followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')
	
	class Meta:
		unique_together = ('followee', 'follower')  # only one followee can be followed by one follower

	