from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hotels', views.hotels, name='hotels'),
    path('hotel', views.hotel, name='hotel'),
    path('booking', views.booking, name='booking'),
    path('bill/<pk>', views.bill, name='bill'),
    path('logout', views.logout_user, name='logout'),
]