import hashlib
import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from response.models import Comment, Like, Dislike
from django.dispatch import receiver


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
	
	def save(self, *args, **kwargs):
		if self.answer:
			md5 = hashlib.md5()
			md5.update(self.answer.encode())
			self.answer = md5.hexdigest()
		super().save(*args, **kwargs)
	
	
class Follow(models.Model):
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
	followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')
	
	class Meta:
		unique_together = ('followee', 'follower')  # only one followee can be followed by one follower

	
# del like, dislike before del user
@receiver(pre_delete, sender=User)
def del_like_dislike_comment(sender, instance, **kwargs):
	from response.models import Comment, Like, Dislike
	Like.objects.filter(obj_type=4, obj_id=instance.id).delete()
	Dislike.objects.filter(obj_type=4, obj_id=instance.id).delete()
	
	
# del the file of avatar when user is deleted
# and the file is not the default avatar
@receiver(pre_delete, sender=User)
def del_avatar(sender, instance, **kwargs):
	if instance.avatar.name != 'avatar/default.jpg' and User.objects.filter(avatar=instance.avatar).count() == 1:
		if os.path.isfile(instance.avatar.path):
			instance.avatar.delete(False)
	