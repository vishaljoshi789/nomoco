from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hotels', views.hotels, name='hotels'),
    path('hotel', views.hotel, name='hotel'),
    path('booking', views.booking, name='booking'),
    path('view_booking', views.view_booking, 
    name='view_booking'),
    path('account', views.account, name='account'),
    path('bill/<pk>', views.bill, name='bill'),
    path('logout', views.logout_user, name='logout'),
    path('login', views.user_login, name='login'),
    path('verify_user', views.user_login_verify, name='verify_user')
]