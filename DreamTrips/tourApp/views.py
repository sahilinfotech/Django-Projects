
from django.shortcuts import render, redirect
from DreamTrips import *
from tourApp.models import *
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


def tourFun(request):
    context = {
        "header": "header header-dark",
        "mainheaderClass": "nav-brand static-show",
        "headerClass": "mob-show",
        "listheader": "list-buttons light",
        "alistheader": "",
    }
    try:
        userDetails = request.session.get("userinfo")
        Destinationdata = DestinationModel.objects.filter(Destination_is_active=True)
        
        
        Destinationstay_with_price = []
        for destination in Destinationdata:
            destinationstay = DestinationstayModel.objects.filter(Destination=destination).first()
            if destinationstay:
                random_reviews = random.randint(1000, 5000)
                random_rating = round(random.uniform(3.0, 5.0), 1)
                Destinationstay_with_price.append({
                    'Destinationstay_id': destinationstay.Destinationstay_id,
                    'Destination': destinationstay.Destination,
                    'Destinationstay_price': destinationstay.Destinationstay_price,
                    'Destinationstay_parking_fees' :destinationstay.Destinationstay_parking_fees,
                    'Destinationstay_services' :destinationstay.Destinationstay_services,
                    'Destinationstay_meal_plan' :destinationstay.Destinationstay_meal_plan,
                    'Destinationstay_dinner' :destinationstay.Destinationstay_dinner,
                    'Destinationstay_lunch' :destinationstay.Destinationstay_lunch,
                    'Destinationstay_breakfast' :destinationstay.Destinationstay_breakfast,
                    'random_reviews': random_reviews,
                    'random_rating': random_rating,

                })
                print(Destinationstay_with_price , "==================")

        if userDetails:
            return render(request, 'tour_list.html', {"Destinationstay_with_price": Destinationstay_with_price, "Destinationdata": Destinationdata, "userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'tour_list.html', {"Destinationstay_with_price": Destinationstay_with_price, "Destinationdata": Destinationdata, "context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')

def tourdetailFun(request, Destination_id):
    context = {
        "header": "header header-dark",
        "mainheaderClass": "nav-brand static-show",
        "headerClass": "mob-show",
        "listheader": "list-buttons light",
        "alistheader": "",
    }
    try:
        userDetails = request.session.get("userinfo")
        
        Destinationdata = DestinationModel.objects.get(pk=Destination_id)
        request.session["selected_destination_id"] = Destinationdata.Destination_id
        Destinationstaydata = DestinationstayModel.objects.filter(Destination=Destinationdata).filter(Destinationstay_is_active = True).values()

        request.session["selected_destinationstay_id"] = Destinationstaydata[0]['Destinationstay_id']




        if userDetails:
        
            return render(request, 'tour_detail.html', {"Destinationstaydata": Destinationstaydata, "Destinationdata": Destinationdata, "userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'tour_detail.html', {"Destinationstaydata": Destinationstaydata, "Destinationdata": Destinationdata,"context": context, "flag": 0})
    
    except Exception as e:
        print(e)
        return render(request, 'error404.html')

    
  


