from django.db import models
from django.contrib.auth.models import AbstractUser

def hotel_directory_path(instance, filename):
    return 'hotel_img/{0}/{1}'.format(instance.hotel_name, filename)
def hotel_img_directory_path(instance, filename):
    return 'hotel_img/{0}/{1}'.format(instance.hotel.hotel_name, filename)
def userID_directory_path(instance, filename):
    return 'user/{0}/{1}'.format(instance.phone, filename)
def designation_directory_path(instance, filename):
    return 'designation/{0}'.format(filename)

# Create your models here.

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=255, blank=True) 
    address = models.CharField(max_length=500, blank=True)
    price = models.CharField(max_length=255,    blank=True)
    offer_price = models.CharField(max_length=255, blank=True)
    hour_1_price = models.CharField(max_length=255, blank=True, default="149")
    hour_2_price = models.CharField(max_length=255, blank=True, default="249")
    hour_3_price = models.CharField(max_length=255, blank=True, default="349")
    hour_4_price = models.CharField(max_length=255, blank=True, default="400")
    poster = models.ImageField(upload_to = hotel_directory_path)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    safety = models.BooleanField(default=True) 
    privacy = models.BooleanField(default=True) 
    security = models.BooleanField(default=True)
    
    available_from = models.TimeField(blank=True)
    available_to = models.TimeField(blank=True)
    hotel_phone = models.CharField(max_length=255, blank=True)
    hotel_email = models.CharField(max_length=255, blank=True) 

    def __str__(self):
        return self.hotel_name 

class Hotel_Image(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='hotel_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hotel_img_directory_path, blank=True)
    img_caption = models.CharField(max_length=255, blank=True)

class Near_by(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="near_by", on_delete=models.CASCADE)
    reference_name = models.CharField(max_length=255, blank=True)
    reference_distance = models.CharField(max_length=255, blank=True)

class User(AbstractUser):
    name = models.CharField(max_length= 100, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=12, blank=True)
    # id_proof = models.ImageField(upload_to = userID_directory_path)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =  []

    def __str__(self):
        return str(self.username)


class Designation(models.Model):
    name = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to = designation_directory_path)
    footer = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    hours = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    child_count = models.CharField(max_length=255, blank=True, null=True)
    adult_count = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.hotel.hotel_name
