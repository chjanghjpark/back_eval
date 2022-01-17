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
	place_id = models.CharField(max_length=16, primary_key=True)
	# store_name = models.CharField(max_length=64)
	place_name = models.CharField(max_length=64)
	# address = models.CharField(max_length=128, primary_key=True)
	address_name = models.CharField(max_length=128)
	road_address_name = models.CharField(max_length=128)
	# latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True)
	x = models.CharField(max_length=32)
	# longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True)
	y = models.CharField(max_length=32)
	area = models.CharField(max_length=8, blank=True)
	district = models.CharField(max_length=8, blank=True)
	# store_type = models.CharField(max_length=8, blank=True)
	category_group_name = models.CharField(max_length=8, blank=True)
	place_url = models.CharField(max_length=128)
	phone = models.CharField(max_length=32)
	category_group_code = models.CharField(max_length=8, blank=True)

	def natural_key(self):
		return ({"id": self.place_id, "place_name": self.place_name, "address_name": self.address_name, "road_address_name": self.road_address_name, \
		"x": self.x, "y": self.y, "area": self.area, "district": self.district, "category_group_name": self.category_group_name, "place_url": self.place_url, \
		"phone": self.phone, "category_group_code": self.category_group_code})

class Evaluate(models.Model):
	user = models.ForeignKey(User, related_name="user_001", on_delete=models.CASCADE, db_column="user")
	store = models.ForeignKey(Store, related_name="store_001", on_delete=models.CASCADE, db_column="place_id")
	star = models.SmallIntegerField(blank=True)
	content = models.TextField(blank=True)
	# iamge = models.ImageField(blank=True)
	write_time = models.DateField(auto_now_add=True)
	fix_time = models.DateField(auto_now=True)
	invited_date = models.DateTimeField(blank=True)
	open_close = models.BooleanField()

class Comment(models.Model):
	user = models.ForeignKey(User, related_name="user_002", on_delete=models.CASCADE, db_column="user")
	evaluate = models.ForeignKey(Evaluate, related_name="store_002", on_delete=models.CASCADE, db_column="place_id")
	content = models.CharField(max_length=256)
	write_time = models.DateField(auto_now_add=True)
	fix_time = models.DateField(auto_now=True)

