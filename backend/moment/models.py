from django.db import models

# Create your models here.


class Moment(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	tot_like = models.IntegerField(default=0)
	tot_comment = models.IntegerField(default=0)
	tot_dislike = models.IntegerField(default=0)

	def __str__(self):
		return self.content
	