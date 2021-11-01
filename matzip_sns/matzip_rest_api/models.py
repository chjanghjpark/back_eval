from django.db import models

# Create your models here.
class Userinfo(models.Model):
	id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length=64)

class Evaluate(models.Model):
	store = models.CharField(max_length=64)
	star = models.CharField(max_length=5)
	user = models.ForeignKey("Userinfo", related_name="user", on_delete=models.CASCADE, db_column="user")
	# comment = models.CharField(max_length=256)
	# adreess = models.CharField(max_length=128)
	# time = models.DateTimeField()
