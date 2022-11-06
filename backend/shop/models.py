from django.db import models


# Create your models here.
class Merchandise(models.Model):
	name = models.CharField(max_length=512)
	# ----------------- image -----------------
	price = models.FloatField()
	