from django.shortcuts import render, HttpResponse, redirect
from .models import *               #import ALL models
from django.contrib import messages #validation
import bcrypt                       #password encryption
from django.conf import settings    #map settings
from datetime import datetime       #events/activities date -time



def index(request):  
    # context = {
    #     #no models yet
    # }
    return render(request, 'index.html')