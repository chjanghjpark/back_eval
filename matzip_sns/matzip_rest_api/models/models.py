from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Userinfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	login_site = models.CharField(max_length=64)
	# profile_image = models.ImageField(blank=True)
	introduce = models.CharField(max_length=256)
	area = models.CharField(max_length=8)

class Store(models.Model):
	store_name = models.CharField(max_length=64)
	address = models.CharField(max_length=128, primary_key=True)
	latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True)
	longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True)
	area = models.CharField(max_length=8)
	district = models.CharField(max_length=8)
	store_type = models.CharField(max_length=8, blank=True)


class Evaluate(models.Model):
	user = models.ForeignKey(User, related_name="user_001", on_delete=models.CASCADE, db_column="user")
	store = models.ForeignKey(Store, related_name="store_001", on_delete=models.CASCADE, db_column="store_name")
	star = models.SmallIntegerField(blank=True)
	content = models.TextField(blank=True)
	# iamge = models.ImageField(blank=True)
	write_time = models.DateField(auto_now_add=True)
	fix_time = models.DateField(auto_now=True)
	invited_date = models.DateTimeField(blank=True)
	open_close = models.BooleanField()

class Comment(models.Model):
	user = models.ForeignKey(User, related_name="user_002", on_delete=models.CASCADE, db_column="user")
	evaluate = models.ForeignKey(Evaluate, related_name="store_002", on_delete=models.CASCADE, db_column="store")
	content = models.CharField(max_length=256)
	write_time = models.DateField(auto_now_add=True)
	fix_time = models.DateField(auto_now=True)
