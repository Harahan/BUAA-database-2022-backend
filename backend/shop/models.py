from django.db import models


# Create your models here.
class Merchandise(models.Model):
	name = models.CharField(max_length=512)
	image = models.ImageField(upload_to='merchandise', default='merchandise/default.jpg')
	price = models.FloatField()
	tot_like = models.IntegerField(default=0)
	tot_dislike = models.IntegerField(default=0)
	tot_comment = models.IntegerField(default=0)
	username = models.ForeignKey('user.User', on_delete=models.CASCADE)  # the user
	time = models.DateTimeField(auto_now=True)
	