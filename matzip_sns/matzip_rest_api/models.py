from django.db import models

# Create your models here.
class Evaluate(models.Model):
	store = models.CharField(max_length=64)
	star = models.CharField(max_length=5)
	# comment = models.CharField(max_length=256)
	# adreess = models.CharField(max_length=128)
	# time = models.DateTimeField()
