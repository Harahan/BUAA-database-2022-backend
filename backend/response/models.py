from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
# from user.models import User
from moment.models import Moment
from blog.models import Article
from shop.models import Merchandise
# Create your models here.


class Comment(models.Model):
	TYPE = (
		(0, 'moment'),
		(1, 'article'),
		(2, 'merchandise'),
		# (3, 'comment'),
	)
	
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	obj_type = models.IntegerField(max_length=10, choices=TYPE)
	obj_id = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	tot_like = models.IntegerField(default=0)
	tot_dislike = models.IntegerField(default=0)

	def __str__(self):
		return self.content
	
	
class Like(models.Model):
	TYPE = (
		(0, 'moment'),
		(1, 'article'),
		(2, 'comment'),
		(3, 'merchandise'),
		(4, 'user'),
	)
	
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	obj_type = models.IntegerField(max_length=10, choices=TYPE)
	obj_id = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)


class Dislike(models.Model):
	TYPE = (
		(0, 'moment'),
		(1, 'article'),
		(2, 'comment'),
		(3, 'merchandise'),
		(4, 'user'),
	)
	
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	obj_type = models.IntegerField(max_length=10, choices=TYPE)
	obj_id = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)
	

@receiver(post_save, sender=Like)
def like_post_save(sender, instance, created, **kwargs):
	if created:
		from user.models import User
		x = [Moment, Article, Comment, Merchandise, User]
		if not x[int(instance.obj_type)].objects.filter(id=instance.obj_id).exists():
			return
		obj = x[int(instance.obj_type)].objects.get(id=instance.obj_id)
		obj.tot_like += 1
		obj.save()
		

@receiver(post_delete, sender=Like)
def like_post_delete(sender, instance, **kwargs):
	from user.models import User
	x = [Moment, Article, Comment, Merchandise, User]
	if not x[int(instance.obj_type)].objects.filter(id=instance.obj_id).exists():
		return
	obj = x[int(instance.obj_type)].objects.get(id=instance.obj_id)
	obj.tot_like -= 1
	obj.save()
	
	
@receiver(post_save, sender=Dislike)
def dislike_post_save(sender, instance, created, **kwargs):
	if created:
		from user.models import User
		x = [Moment, Article, Comment, Merchandise, User]
		if not x[int(instance.obj_type)].objects.filter(id=instance.obj_id).exists():
			return
		obj = x[int(instance.obj_type)].objects.get(id=instance.obj_id)
		obj.tot_dislike += 1
		obj.save()
		
		
@receiver(post_delete, sender=Dislike)
def dislike_post_delete(sender, instance, **kwargs):
	from user.models import User
	x = [Moment, Article, Comment, Merchandise, User]
	if not x[int(instance.obj_type)].objects.filter(id=instance.obj_id).exists():
		return
	obj = x[int(instance.obj_type)].objects.get(id=instance.obj_id)
	obj.tot_dislike -= 1
	obj.save()
	
	
@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
	if created:
		x = [Moment, Article, Merchandise]
		if not x[int(instance.obj_type)].objects.filter(id=instance.obj_id).exists():
			return
		obj = x[int(instance.obj_type)].objects.get(id=instance.obj_id)
		obj.tot_comment += 1
		obj.save()
		
		
@receiver(post_delete, sender=Comment)
def comment_post_delete(sender, instance, **kwargs):
	x = [Moment, Article, Merchandise]
	if not x[int(instance.obj_type)].objects.filter(id=instance.obj_id).exists():
		return
	obj = x[int(instance.obj_type)].objects.get(id=instance.obj_id)
	obj.tot_comment -= 1
	obj.save()


# del like, dislike before the comment is deleted
@receiver(pre_delete, sender=Comment)
def del_like_dislike(sender, instance, **kwargs):
	Like.objects.filter(obj_type=2, obj_id=instance.id).delete()
	Dislike.objects.filter(obj_type=2, obj_id=instance.id).delete()
	

