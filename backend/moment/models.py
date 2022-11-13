from django.db import models

# Create your models here.


class Moment(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()

	def __str__(self):
		return self.content
	