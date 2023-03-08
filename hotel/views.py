from django.shortcuts import render, redirect
import pyotp
from .models import Designation, Hotel, User, Booking
from itertools import chain
from django.contrib.auth import login, logout, authenticate
from django.conf import settings 
from django.core.mail import send_mail 
import random

# Create your views here.
designation = Designation.objects.all()

desig = designation

hotp = pyotp.HOTP('base32secret323255nomoco')

def verify_otp(password, id):
    return hotp.verify(password, id)

def opt_generator(id):
    return hotp.at(id)

def index(request):
    # otp = opt_generator(5)
    context = {}
    context['style'] = 'index.css'
    context['designation'] = designation
    return render(request, 'hotel/index.html', context)

def hotels(request):
    context = {}
    context['designation'] = desig
    context['hotels'] = 'no q'
    if request.GET.get('designation'):
        designation = request.GET.get('designation')
        date = request.GET.get('date')
        time = request.GET.get('time')
        hotels = Hotel.objects.all()
        if time != 'None' and time != '' and time:
            hotels = hotels.filter(available_to__gte=time)
            hotels = hotels.filter(available_from__lte=time)
        hotels_byname = hotels.filter(hotel_name__icontains=designation)
        hotels_byaddress = hotels.filter(address__icontains=designation)
        # hotels_bynearby = hotels.near_by.filter(reference_name__icontains=designation)
        hotels = set(chain(hotels_byname, hotels_byaddress,))
        print(hotels)
        context['hotels'] = hotels
        context['date'] = date
        context['time'] = time
        context['desc'] = designation
    context['style'] = 'hotels.css'
    return render(request, 'hotel/hotels.html', context)

def hotel(request):
    context = {}
    context['designation'] = designation

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
    context['designation'] = designation

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
            
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            key = random.randint(0, 999999)                
            otp = opt_generator(key)
            password = otp
            id_front = request.POST.get('front_id')
            id_back = request.POST.get('back_id')
            username = email
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                print(user)
                user.name = name
                user.phone = phone
                user.save()
            else:
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
    context['designation'] = designation

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

def view_booking(request):
    context = {}  
    context['designation'] = designation
    if request.user.is_authenticated:
        bookings = Booking.objects.all().filter(user=request.user)
        context['bookings'] = bookings
    return render(request, 'hotel/view_booking.html', context)
    
def account(request):
     return render(request, 'hotel/account.html')

def user_login(request):
     if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            ctx = {}
            key = random.randint(0, 999999)
            otp = opt_generator(key)
            # ctx['otp'] = otp
            ctx['email'] = email
            subject = "Login to NOMOCO"
            message = f'Your OTP for email {email} is {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            mail = send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recipient_list)
            if mail:
                user = User.objects.get(email=email)
                user.set_password(otp)
                user.save()
                return render(request, 'hotel/login_verify.html', ctx)
     return render(request, 'hotel/login.html')

def user_login_verify(request):
     if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        user = authenticate(request, username = email, password = otp)
        if user is not None:
            login(request, user)
            return redirect('account')

    