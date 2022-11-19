from django.db import models

COLOR = {
	'#00AB55': 1,	 # green
	'#000000': 2,	 # black
	'#FFFFFF': 4,	 # white
	'#FFC0CB': 8,	 # pink
	'#FF4842': 16,	 # red
	'#1890FF': 32,   # blue
	'#94D82D': 64,	 # green
	'#FFC107': 128,  # yellow
}


# Create your models here.
class Merchandise(models.Model):
	TYPE = (
		("food", "food"),
		("clothing", "clothing"),
		("book", "book"),
		("decoration", "decoration"),
		("digital", "digital"),
		("over", "other")
	)
	
	name = models.CharField(max_length=512)
	image = models.ImageField(upload_to='merchandise', default='merchandise/default.jpg')
	price = models.FloatField(default=0)
	tot_like = models.IntegerField(default=0)
	tot_dislike = models.IntegerField(default=0)
	tot_comment = models.IntegerField(default=0)
	username = models.ForeignKey('user.User', on_delete=models.CASCADE)  # the user
	time = models.DateTimeField(auto_now=True)
	description = models.CharField(max_length=1024, default="", blank=True)
	category = models.CharField(max_length=20, choices=TYPE, default="other")
	color = models.IntegerField(default=0)
	deliveryLocation = models.CharField(max_length=1024, default="", blank=True)
	deliveryTime = models.CharField(max_length=200, default=None, blank=True, null=True)
	priceSale = models.FloatField(default=0)
	
	