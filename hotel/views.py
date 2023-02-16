from django.shortcuts import render
import pyotp

# Create your views here.
hotp = pyotp.HOTP('base32secret323255nomoco')

def verify_otp(password, id):
    return hotp.verify(password, id)

def opt_generator(id):
    return hotp.at(id)

def index(request):
    # otp = opt_generator(5)
    context = {}
    context['style'] = 'index.css'
    return render(request, 'hotel/index.html', context)

def hotels(request):
    context = {}
    context['hotels'] = 'no q'
    if request.GET.get('q'):
        context['hotels'] = request.GET['q']
    context['style'] = 'hotels.css'
    return render(request, 'hotel/hotels.html', context)

def hotel(request):
    context = {}
    context['style'] = 'hotel.css'
    return render(request, 'hotel/hotel.html', context)
    