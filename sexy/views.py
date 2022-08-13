#Import models
from profil.models import User, Follower

#Import others Stuffs
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

#import boto&client for sending otp
from random import randint
# from http import client
# import boto3

# Home page view
def home(request):
    return render(request, "home.html", {})

# Login view
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        # In order to sign in with phone number, we get phone from request
        phone = request.POST["phone"]
        password = request.POST["password"]

        # Try to get user associate with previous phone numer
        try:
            person = User.objects.get(phone_number = phone)
            user = authenticate(request, username=person.username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return render(request, "login.html", {
                    "message": "Mot de passe INCORRECT"
                })
        except Exception as e:
            return render(request, "login.html", {
                    "message": "Ce numero n'existe pas"
                })

    else:
        return render(request, "login.html", {})

#Register view
#The register methos has 3 steps, 
#first step is register1 where we ask user his phone number
def register1(request):

    if request.method == "POST":
        
        pays = request.POST["pays"]
        phone = request.POST["phone"]
        sited = User(username='test', country=pays)
        
        
        # Ensure no one has this phone
        try:
            user = User.objects.get(phone=phone)
            return render(request, "register1.html", {
                "message": "Ce numero existe déja!.",
                "phone": phone,
                "pays": pays,
                "sited": sited,
            })
        except Exception as e:
            #send sms using boto3 an amazon SNS

            code = randint(10000, 50000)
            # client = boto3.client('sns', 'eu-west-3')
            # client.publish(PhoneNumber='+237690638290', Message='Votre code est : '+str(code))

            return render(request, "register2.html", {
                "phone": phone,
                "pays": pays,
                "code": code,
                "sited": sited,
            })
    else:
       
        return render(request, "register1.html",)

def register2(request):
    if request.method == "POST":
        
        pays = request.POST["pays"]
        phone = request.POST["phone"]
        code1 = request.POST["code1"]
        code2 = request.POST["code2"]
        
        if code1 == code2:
            return render(request, "register3.html", {
                "phone": phone,
                "pays": pays,
            })

        else:
            return render(request, "register2.html", {
                "message": "Code incorrect!.",
                "phone": phone,
                "pays": pays,
                "code":code2,
            })
   
    else:
        return render(request, "register2.html",)

def register3(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        pays = request.POST["pays"]
        phone = request.POST["phone"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register3.html", {
                "message": "Les mots de passe ne correspondent pas",
                "phone": phone,
                "pays": pays,
                "username": username
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, country=pays, phone=phone, password=password, devoile=password)         
            user.save()
            Follower.objects.create(user=user)
        except IntegrityError:
            return render(request, "register3.html", {
                "message": "Ce nom est déja utilisé.",
                "phone": phone,
                "pays": pays,
                "username": username,
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "register3.html")
 
