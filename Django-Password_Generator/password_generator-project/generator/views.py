from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.


def home(request):
    return render(request, "generator/home.html")


def about(request):
    return render(request, "generator/about.html")


def password(request):
    pwd = ""

    length = int(request.GET.get("length", 12))
    uppercase = 0 if request.GET.get("UPPERCASE", "off") == "off" else 1
    nums = 0 if request.GET.get("Numbers", "off") == "off" else 1
    spl = 0 if request.GET.get("special", "off") == "off" else 1

    lowerLetters = list("abcdefghijklmnopqrstuvwxyz")
    upperLetters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numsList = list("0123456789")
    splList = list("!@#$%^&*()")

    if uppercase:
        lowerLetters.extend(upperLetters)
    if nums:
        lowerLetters.extend(numsList)
    if spl:
        lowerLetters.extend(splList)

    for i in range(length):
        pwd += random.choice(lowerLetters)

    return render(request, "generator/password.html", {"password": pwd})
