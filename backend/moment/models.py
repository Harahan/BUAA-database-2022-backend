from django.db import models

# Create your models here.
from django.db.models.signals import pre_delete
# from response.models import Comment, Like, Dislike
from django.dispatch import receiver


class Moment(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	tot_like = models.IntegerField(default=0)
	tot_comment = models.IntegerField(default=0)
	tot_dislike = models.IntegerField(default=0)

	def __str__(self):
		return self.content
	
	
# del like/dislike/comment when moment is deleted
@receiver(pre_delete, sender=Moment)
def delete_like_dislike_comment(sender, instance, **kwargs):
	from response.models import Comment, Like, Dislike
	Like.objects.filter(obj_type=0, obj_id=instance.id).delete()
	Dislike.objects.filter(obj_type=0, obj_id=instance.id).delete()
	Comment.objects.filter(obj_type=0, obj_id=instance.id).delete()