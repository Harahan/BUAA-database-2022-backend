from django.db import models

# Create your models here.


class Group(models.Model):
	name = models.CharField(max_length=100)
	# description = models.CharField(max_length=200)
	member = models.ManyToManyField('user.User', related_name='group_member')
	owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='group_owner')
	time = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.name
	