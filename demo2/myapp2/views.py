from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, "home.html")

def day1(request):
    return render(request, "day1.html")

def day2(request):
    return render(request, "day2.html")

def day3(request):
    return render(request, "day3.html")

def day4(request):
    return render(request, "day4.html")

def top5(request):
    return render(request, "top5.html")

def base(request):
    return render(request, "base.html")

# Create your views here.
