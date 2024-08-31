
from django.shortcuts import render, redirect
from DreamTrips import *
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

# def flightFun(request):
#     context = {
#             "header" : "header header-dark",
#             "mainheaderClass" : "nav-brand static-show",
#             "headerClass" : "mob-show",
#             "listheader" : "list-buttons light",
#             "alistheader" : "",

#         }
#     try:
#         userDetails = request.session.get("userinfo")
#         flightdata = flightModel.objects.filter(flight_is_active=True).values()
#         flightdetailsdata = flightDetailsModel.objects.filter(flightDetails_is_active=True)
#         flightFacilitiesdata = flightFacilitiesModel.objects.filter(flightFacilities_is_active=True)
#         flightdepaturetime = flightDetailsModel.objects.values('flightDetails_departure_time').distinct()
#         flightdestinationtime = flightDetailsModel.objects.values('flightDetails_destination_time').distinct()
#         print(flightdestinationtime , "kkkkkkkkk")

#         print(flightdetailsdata)
        
#         if userDetails:
#             return render(request, 'flight_list.html', {"flightdestinationtime":flightdestinationtime,"flightdepaturetime":flightdepaturetime,"flightdata":flightdata,"flightFacilitiesdata":flightFacilitiesdata,"flightdetailsdata" : flightdetailsdata,"userDetails": userDetails, "context": context, "flag": 1})
#         else:
#             return render(request, 'flight_list.html', {"flightdestinationtime":flightdestinationtime,"flightdepaturetime":flightdepaturetime,"flightdata":flightdata,"flightFacilitiesdata":flightFacilitiesdata,"flightdetailsdata" : flightdetailsdata,"context": context, "flag": 0})
#     except Exception as e:
#         print(e)
#         return render(request, 'error404.html')

def flightFun(request):
    context = {
        "header": "header header-dark",
        "mainheaderClass": "nav-brand static-show",
        "headerClass": "mob-show",
        "listheader": "list-buttons light",
        "alistheader": "",
    }
    try:
        userDetails = request.session.get("userinfo")
        flightdata = flightModel.objects.filter(flight_is_active=True).values()
        flightdetailsdata = flightDetailsModel.objects.filter(flightDetails_is_active=True)
        flightFacilitiesdata = flightFacilitiesModel.objects.filter(flightFacilities_is_active=True)
        flightdepaturetime = flightDetailsModel.objects.values('flightDetails_departure_time').distinct()
        flightdestinationtime = flightDetailsModel.objects.values('flightDetails_destination_time').distinct()

        if userDetails:
            return render(request, 'flight_list.html', {
                "flightdestinationtime": flightdestinationtime,
                "flightdepaturetime": flightdepaturetime,
                "flightdata": flightdata,
                "flightFacilitiesdata": flightFacilitiesdata,
                "flightdetailsdata": flightdetailsdata,
                "userDetails": userDetails,
                "context": context,
                "flag": 1
            })
        else:
            return render(request, 'flight_list.html', {
                "flightdestinationtime": flightdestinationtime,
                "flightdepaturetime": flightdepaturetime,
                "flightdata": flightdata,
                "flightFacilitiesdata": flightFacilitiesdata,
                "flightdetailsdata": flightdetailsdata,
                "context": context,
                "flag": 0
            })
    except Exception as e:
        print(e)
        return render(request, 'error404.html')

def filter_flights(request):
    departure_times = request.GET.getlist('departure_times[]')
    destination_times = request.GET.getlist('destination_times[]')
    facilities = request.GET.getlist('facilities[]')
    airlines = request.GET.getlist('airlines[]')

    flights = flightDetailsModel.objects.filter(flightDetails_is_active=True)

    if departure_times:
        flights = flights.filter(flightDetails_departure_time__in=departure_times)
    if destination_times:
        flights = flights.filter(flightDetails_destination_time__in=destination_times)
    if facilities:
        flights = flights.filter(flight__flightFacilities__flightFacilities_name__in=facilities)
    if airlines:
        flights = flights.filter(flight__flight_name__in=airlines)

    flights = flights.values()
    return JsonResponse(list(flights), safe=False)

def flightdetailFun(request, flightClass_id):
    context = {
        "header": "header header-dark",
        "mainheaderClass": "nav-brand static-show",
        "headerClass": "mob-show",
        "listheader": "list-buttons light",
        "alistheader": "",
    }
    try:
        # Get user info from session
        userDetails = request.session.get("userinfo")

        flightclassdata = flightClassModel.objects.get(pk=flightClass_id)
        request.session["selected_flight_id"] = flightclassdata.flightClass_id

        if userDetails:
            return render(request, 'flight_detail.html', {"flightclassdata": flightclassdata, "userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'flight_detail.html', {"flightclassdata": flightclassdata, "context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')

def flightclassFun(request, flightDetails_id):
    context = {
        "header": "header header-dark",
        "mainheaderClass": "nav-brand static-show",
        "headerClass": "mob-show",
        "listheader": "list-buttons light",
        "alistheader": "",
    }
    try:
        # Get user info from session
        userDetails = request.session.get("userinfo")

        flightdetailsdata = flightDetailsModel.objects.get(pk=flightDetails_id)
        flightclassdata = flightClassModel.objects.filter(flightDetails=flightdetailsdata, flightClass_is_active=True)

        if userDetails:
            return render(request, 'flight_class.html', {"flightclassdata": flightclassdata, "flightdetailsdata": flightdetailsdata, "userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'flight_class.html', {"flightclassdata": flightclassdata, "flightdetailsdata": flightdetailsdata, "context": context, "flag": 0})

    except Exception as e:
        print(e)
        return render(request, 'error404.html')

