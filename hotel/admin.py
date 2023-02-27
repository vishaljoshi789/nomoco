from django.contrib import admin
from .models import Hotel, User, Hotel_Image, Designation, Near_by, Booking
# Register your models here.

class HotelImageInline(admin.TabularInline):
    model = Hotel_Image
    extra = 3

class HotelNearByInline(admin.TabularInline):
    model = Near_by
    extra = 3

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelNearByInline, HotelImageInline]


admin.site.register(Hotel, HotelAdmin)
admin.site.register(User)
admin.site.register(Designation)
admin.site.register(Booking)

