
from django.shortcuts import render, redirect
from DreamTrips import *
from DreamTrips.models import *
from tourApp.models import *
from flightApp.models import *
from hotelApp.models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  #for File storage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
import random
import string
import os
import io
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



def indexFun(request):
    context = {
        "header": "header header-transparent theme",
        "mainheaderClass": "nav-brand static-show",
        "headerClass": "mob-show",
        "listheader": "list-buttons light",
        "alistheader": "",
    }

    try:
        userDetails = request.session.get("userinfo")

        Destinationdata = DestinationModel.objects.filter(Destination_is_active=True).values()
        Destinationstaydata = DestinationstayModel.objects.filter(Destinationstay_is_active=True).values()
        destinationHoteldata = destinationHotelModel.objects.filter(destinationHotel_is_active=True)

        for hotel in destinationHoteldata:
            hotel.images = hotel.destinationhotelimagemodel_set.first()
            print(hotel.images)

        if userDetails:
            return render(request, 'index.html', {"destinationHoteldata": destinationHoteldata, "Destinationstaydata": Destinationstaydata, "Destinationdata": Destinationdata, "userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'index.html', {"destinationHoteldata": destinationHoteldata, "Destinationstaydata": Destinationstaydata, "Destinationdata": Destinationdata, "context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')
 
def contactUsFun(request):
    context = {
        "header": "header header-theme",
        "mainheaderClass": "",
        "headerClass": "",
        "listheader": "list-buttons light",
        "alistheader": "bg-primary",
    }
    try:
        userDetails = request.session.get("userinfo")
        
        if userDetails:
            return render(request, 'contact.html', {"userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'contact.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')
    
def helpCenterFun(request):
    context = {
            "header" : "header header-light",
            "mainheaderClass" : "",
            "headerClass" : "",
            "listheader" : "list-buttons",
            "alistheader" : "bg-primary",

        }
    try:
        userDetails = request.session.get("userinfo")
        
        if userDetails:
            return render(request, 'help_center.html', {"userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'help_center.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')
    
def contactUsRegisterFun(request):
    context = {
        "header": "header header-theme",
        "mainheaderClass": "",
        "headerClass": "",
        "listheader": "list-buttons light",
        "alistheader": "bg-primary",
    }
    try:
            
        if request.method == "POST":
            contactUs_name_ = request.POST.get('contactUsName')
            contactUs_phone_ = request.POST.get('contactUsPhone')
            contactUs_query_ = request.POST.get('contactUsQuery')
            contactUs_subject_ = request.POST.get('contactUsSubject')
            contactUs_email_ = request.POST.get('contactUsEmail')
            
            if len(contactUs_name_) <= 0:
                error = 'Please Enter Contact First Name !!'
                return render(request, 'contact.html', {"error":error, "flag" : 0})
            
            if not contactUs_name_.isalpha():
                error =  'Please enter a valid First Name (only text characters are filterowed)'
                return render(request, 'contact.html', {"error":error, "flag" : 0})

            if len(contactUs_phone_) <= 0:
                error = 'Please Enter Contact Us Subject !!'
                return render(request, 'contact.html', {"error":error, "flag" : 0})
            if not contactUs_phone_.isdigit():
                error =  'Please enter a valid Phone No. (only digits are filterowed)'
                return render(request, 'contact.html', {"error":error, "flag" : 0})
            
            if len(contactUs_subject_) <= 0:
                error = 'Please Enter Contact Us Subject !!'
                return render(request, 'contact.html', {"error":error, "flag" : 0})
            
            if len(contactUs_email_) <= 0:
                error = 'Please Enter Contact Us Email !!'
                return render(request, 'contact.html', {"error":error, "flag" : 0})
            try:
                validate_email(contactUs_email_)
            except ValidationError:
                error =  'Please enter a valid email address!'
                return render(request, 'contact.html', {"error":error, "flag" : 0})
            
            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            uniqueID = "DreamTrips_ContactUs_" + randomstr

            
            contactUs = contactUsModel(
                contactUs_id = uniqueID,
                contactUs_name = contactUs_name_,
                contactUs_phone = contactUs_phone_,
                contactUs_query = contactUs_query_,
                contactUs_email = contactUs_email_,
                contactUs_subject = contactUs_subject_,
                
            )
        
            contactUs.save()

            if contactUs.contactUs_id:

                return render(request, 'contact.html', {"context":context, "flag" : 1})
            else:
                error =  "Something is wrong!!"
                return render(request, 'contact.html', {"context":context,"error":error, "flag" : 0})
                
    except Exception as e:
        print(e)
        return render(request, 'error404.html')