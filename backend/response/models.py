from django.db import models

# Create your models here.


class Comment(models.Model):
	TYPE = (
		(0, 'moment'),
		(1, 'article'),
		(2, 'merchandise'),
		# (3, 'comment'),
	)
	
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	obj_type = models.CharField(max_length=10, choices=TYPE)
	obj_id = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	tot_like = models.IntegerField(default=0)

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
	obj_type = models.CharField(max_length=10, choices=TYPE)
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
	obj_type = models.CharField(max_length=10, choices=TYPE)
	obj_id = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)
	
