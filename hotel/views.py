from django.shortcuts import render, redirect
import pyotp
from .models import Designation, Hotel, User, Booking
from itertools import chain
from django.contrib.auth import login, logout
from datetime import datetime, timedelta

# Create your views here.
hotp = pyotp.HOTP('base32secret323255nomoco')

def verify_otp(password, id):
    return hotp.verify(password, id)

def opt_generator(id):
    return hotp.at(id)

def index(request):
    # otp = opt_generator(5)
    context = {}
    designation = Designation.objects.all()
    context['style'] = 'index.css'
    context['designation'] = designation
    return render(request, 'hotel/index.html', context)

def hotels(request):
    context = {}
    context['hotels'] = 'no q'
    if request.GET.get('designation'):
        designation = request.GET.get('designation')
        date = request.GET.get('date')
        time = request.GET.get('time')
        print(time)
        hotels = Hotel.objects.all()
        hotels = hotels.filter(available_to__gte=time)
        hotels = hotels.filter(available_from__lte=time)
        hotels_byname = hotels.filter(hotel_name__icontains=designation)
        hotels_byaddress = hotels.filter(address__icontains=designation)
        # hotels_bynearby = hotels.near_by.filter(reference_name__icontains=designation)
        hotels = list(chain(hotels_byname, hotels_byaddress,))
        context['hotels'] = hotels
        context['date'] = date
        context['time'] = time
        context['desc'] = designation
    context['style'] = 'hotels.css'
    return render(request, 'hotel/hotels.html', context)

def hotel(request):
    context = {}
    if request.method == 'GET':
        hotel_id = request.GET.get('id')
        date = request.GET.get('date')
        time = request.GET.get('time')
        hotel = Hotel.objects.get(id=hotel_id)
        hotel_image = hotel.hotel_image.all()
        hotel_nearBy = hotel.near_by.all()
        context['hotel'] = hotel
        context['hotel_image'] = hotel_image
        context['hotel_nearBy'] = hotel_nearBy
        context['date'] = date
        context['time'] = time

    context['style'] = 'hotel.css'
    return render(request, 'hotel/hotel.html', context)

def booking(request):
    context = {}
    if request.method == 'POST':
    
            context['hotel_id'] = request.POST.get('hotel_id')
            context['date'] = request.POST.get('date')
            context['time'] = request.POST.get('time')
            context['hour_count'] = request.POST.get('hour_count')
            context['price'] = request.POST.get('price')
            context['adult_count'] = request.POST.get('adult_count')
            context['child_count'] = request.POST.get('child_count')
            
    if request.POST.get('type') == 'user_registration':
            # if request.POST.get('phone')
            if request.user.is_authenticated:
                 pass
            else:
                name = request.POST.get('name')
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                password = "testpassword"
                id_front = request.POST.get('front_id')
                id_back = request.POST.get('back_id')
                username = phone
                user = User.objects.create_user(name=name, email=email, username=username, phone=phone, password=password)
                user.save()
                login(request, user=user)
            hotel = Hotel.objects.get(id=context['hotel_id'])
            time = context['time']
            hour_count = context['hour_count']
            check_out = time.split(':')
            check_out[0] = int(check_out[0]) + int(hour_count)
            check_out[0] = str(check_out[0])
            check_out = ':'.join(check_out)
            booking = Booking.objects.create(hotel=hotel, user=request.user, time_from=context['time'],time_to=check_out, date=context['date'], hours = context['hour_count'], price=context['price'], child_count=context['child_count'], adult_count=context['adult_count'])
            booking.save()
            return redirect("bill", booking.id)

    context['style'] = 'booking.css'
    return render(request, 'hotel/booking.html', context)

def bill(request, pk):
    context = {}
    bill = Booking.objects.get(id=pk)
    
    context['bill'] = bill
    context['price'] = int(bill.price)
    context['hours'] = int(bill.hours)
    context['max_price'] = 500*context['hours']
    context['discount'] = context['max_price'] - context['price']
    context['total_price'] = (context['price'])+(context['price']*.12).__round__()
    context['style'] = 'bill.css'
    return render(request, 'hotel/bill.html', context)

def logout_user(request):
     logout(request)
     return redirect('index')
    