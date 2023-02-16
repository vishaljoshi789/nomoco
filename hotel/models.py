from django.db import models
from django.contrib.auth.models import AbstractUser

def hotel_directory_path(instance, filename):
    return 'hotel_{0}/{1}'.format(instance.hotel_name, filename)
def userID_directory_path(instance, filename):
    return 'hotel_{0}/{1}'.format(instance.phone, filename)

# Create your models here.

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=255, blank=True) 
    address = models.CharField(max_length=500, blank=True)
    price = models.CharField(max_length=255,    blank=True)
    offer_price = models.CharField(max_length=255, blank=True)
    poster = models.ImageField(upload_to = hotel_directory_path)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    safety = models.BooleanField(default=True) 
    privacy = models.BooleanField(default=True) 
    security = models.BooleanField(default=True)
    near_by = models.TextField(blank=True)
    available_from = models.TimeField(blank=True)
    available_to = models.TimeField(blank=True)
    hotel_phone = models.CharField(max_length=255, blank=True)
    hotel_email = models.CharField(max_length=255, blank=True) 

    def __str__(self):
        return self.hotel_name 

class User(AbstractUser):
    name = models.CharField(max_length= 100, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=12, blank=True)
    id_proof = models.ImageField(upload_to = userID_directory_path)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =  []

    def __str__(self):
        return str(self.username)


# class Booking(models.Model):
#     pass 
