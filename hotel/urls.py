from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hotels', views.hotels, name='hotels'),
    path('hotel', views.hotel, name='hotel'),
]