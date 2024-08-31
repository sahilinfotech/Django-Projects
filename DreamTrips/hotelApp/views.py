
from django.shortcuts import render, redirect
from DreamTrips import *
from hotelApp.models import *
from final_paymentApp.models import *
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

# Create your views here.
def hotelFun(request):
    context = {
        "header": "header header-dark",
        "mainheaderClass": "nav-brand static-show",
        "headerClass": "mob-show",
        "listheader": "list-buttons light",
        "alistheader": "",
    }
    try:
        userDetails = request.session.get("userinfo")
        selected_destinationstay_id = request.session.get('selected_destinationstay_id')
        amenitiesdata = amenitiesModel.objects.filter(amenities_is_active=True)
        roomTypedata = roomTypeModel.objects.filter(roomType_is_active=True)

        # Filter destination hotels based on selected_destinationstay_id
        destinationHoteldata = destinationHotelModel.objects.filter(Destinationstay_id=selected_destinationstay_id,destinationHotel_is_active=True)

        print(destinationHoteldata , "kkkkkkkkkkkkkkk")

        hotel_data_with_random = []

        for hotel in destinationHoteldata:
            random_reviews = random.randint(1000, 5000)
            random_rating = round(random.uniform(3.0, 5.0), 1)
            hotel_data_with_random.append({
                "destinationHotel_id": hotel.destinationHotel_id,
                "destinationHotel_hotel_price": hotel.destinationHotel_hotel_price,
                "destinationHotel_cooling": hotel.destinationHotel_cooling,
                "destinationHotel_eating": hotel.destinationHotel_eating,
                "destinationHotel_hotel_discount": hotel.destinationHotel_hotel_discount,
                "destinationHotel_hotel_name": hotel.destinationHotel_hotel_name,
                "destinationHotel_only_adults": hotel.destinationHotel_only_adults,
                "destinationHotel_parking": hotel.destinationHotel_parking,
                "destinationHotel_pet_allowed": hotel.destinationHotel_pet_allowed,
                "destinationHotel_wifi": hotel.destinationHotel_wifi,
                "destinationHotel_image": hotel.destinationhotelimagemodel_set.first(),
                "random_reviews": random_reviews,
                "random_rating": random_rating
            })
            print(hotel_data_with_random , "llllllllllllllllll")
        if userDetails:
            return render(request, 'hotel_list.html', {
                "hotel_data_with_random": hotel_data_with_random,
                "roomTypedata": roomTypedata,
                "amenitiesdata": amenitiesdata,
                "destinationHoteldata": destinationHoteldata,
                "userDetails": userDetails,
                "context": context,
                "flag": 1
            })
        else:
            return render(request, 'hotel_list.html', {
                "hotel_data_with_random": hotel_data_with_random,
                "roomTypedata": roomTypedata,
                "amenitiesdata": amenitiesdata,
                "destinationHoteldata": destinationHoteldata,
                "context": context,
                "flag": 0
            })
    except Exception as e:
        print(e)
        return render(request, 'error404.html')
   
def hoteldetailFun(request, destinationHotel_id):
    context = {
        "header": "header header-dark",
        "mainheaderClass": "nav-brand static-show",
        "headerClass": "mob-show",
        "listheader": "list-buttons light",
        "alistheader": "",
    }

    try:
        userDetails = request.session.get("userinfo")

        Destinationhoteldata = destinationHotelModel.objects.get(pk=destinationHotel_id)
        request.session["selected_hotel_id"] = Destinationhoteldata.destinationHotel_id
        destinationHotel_data = destinationHotelModel.objects.filter(destinationHotel_id=destinationHotel_id, destinationHotel_is_active=True).values()
        hotelimages = destinationHotelImageModel.objects.filter(destinationHotel=Destinationhoteldata, destinationHotelImage_is_active=True)
        hotelRoomtypedata = hotelRoomTypeModel.objects.filter(destinationHotel=Destinationhoteldata, hotelRoomType_is_active=True).values()
        hotelActivitiesdata = hotelActivitiesModel.objects.filter(destinationHotel=Destinationhoteldata, hotelActivities_is_active=True).values()
        hotelServicedata = hotelServiceModel.objects.filter(destinationHotel=Destinationhoteldata, hotelService_is_active=True).values()
        hotelAmenitiesdata = hotelAmenitiesModel.objects.filter(destinationHotel=Destinationhoteldata, hotelAmenities_is_active=True).values()

        
        roomtype_with_names = []
        for roomtype_data in hotelRoomtypedata:
            amenity_instance = roomTypeModel.objects.get(pk=roomtype_data['roomType_id'])
            roomtype_with_names.append({
                'roomType_id': roomtype_data['roomType_id'],
                'roomType_name': amenity_instance.roomType_name
            })
        
        amenities_with_names = []
        for amenity_data in hotelAmenitiesdata:
            amenity_instance = amenitiesModel.objects.get(pk=amenity_data['amenities_id'])
            amenities_with_names.append({
                'amenities_id': amenity_data['amenities_id'],
                'amenities_name': amenity_instance.amenities_name
            })

        services_with_names = []
        for service_data in hotelServicedata:
            service_instance = serviceModel.objects.get(pk=service_data['service_id'])
            services_with_names.append({
                'service_id': service_data['service_id'],
                'service_name': service_instance.service_name
            })

        activities_with_names = []
        for activity_data in hotelActivitiesdata:
            activity_instance = activitiesModel.objects.get(pk=activity_data['activities_id'])
            activities_with_names.append({
                'activity_id': activity_data['activities_id'],
                'activity_name': activity_instance.activities_name
            })

        if userDetails:
            return render(request, 'hotel_detail.html', {"hotelRoomtypedata":roomtype_with_names,"hotelActivitiesdata": hotelActivitiesdata, "hotelAmenitiesdata": amenities_with_names, "hotelServicedata": services_with_names, "hotelActivitiesdata": activities_with_names, "hotelimages": hotelimages, "destinationHotel_data": destinationHotel_data, "Destinationhoteldata": Destinationhoteldata, "userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'hotel_detail.html', {"hotelRoomtypedata":roomtype_with_names,"hotelActivitiesdata": hotelActivitiesdata, "hotelAmenitiesdata": amenities_with_names, "hotelServicedata": services_with_names, "hotelActivitiesdata": activities_with_names, "hotelimages": hotelimages, "destinationHotel_data": destinationHotel_data, "Destinationhoteldata": Destinationhoteldata, "context": context, "flag": 0})
        
    except Exception as e:
        print(e)
        return render(request, 'error404.html')
