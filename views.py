from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def infoChatter(request):
    return render(request, 'info/infoChatter.html')

def infoLottery(request):
    return render(request, 'info/infoLottery.html')

def infoWeather(request):
    return render(request, 'info/infoWeather.html')