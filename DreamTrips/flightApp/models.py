from django.db import models
from hotelApp.models import *
from userApp.models import *
# Create your models here.

class flightModel(models.Model):
    class Meta:
        db_table = "flight_tb"
    flight_id = models.CharField(default=None, max_length=60, primary_key=True)
    flight_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    flight_icon = models.ImageField(upload_to='flight/')
    flight_is_active = models.BooleanField(default= True)
    flight_created_at = models.DateTimeField(auto_now_add=True)


class flightDetailsModel(models.Model):
    class Meta:
        db_table = "flightDetails_tb"
    flightDetails_id = models.CharField(default=None, max_length=60, primary_key=True)
    flight = models.ForeignKey(flightModel, on_delete=models.CASCADE, default=None)
    flightDetails_status = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_departure_place = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_destination_place = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_departure_time = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_destination_time = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_timeperiod = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_return_departure_place = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_return_destination_place = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_return_departure_time = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_return_destination_time = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_return_timeperiod = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_discount = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_date = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_return_date = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightDetails_is_active = models.BooleanField(default= True)
    flightDetails_created_at = models.DateTimeField(auto_now_add=True)

class flightClassModel(models.Model):
    class Meta:
        db_table = "flightClass_tb"
    flightClass_id = models.CharField(default=None, max_length=60, primary_key=True)
    flightDetails = models.ForeignKey(flightDetailsModel, on_delete=models.CASCADE, default=None)
    flightClass_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightClass_price = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightClass_is_active = models.BooleanField(default= True)
    flightClass_created_at = models.DateTimeField(auto_now_add=True)

class flightFacilitiesModel(models.Model):
    class Meta:
        db_table = "flightFacilities_tb"
    flightFacilities_id = models.CharField(default=None, max_length=60, primary_key=True)
    flightDetails = models.ForeignKey(flightDetailsModel, on_delete=models.CASCADE, default=None)
    flightFacilities_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    flightFacilities_description = models.TextField(default=None, blank=True, null=True)
    flightFacilities_is_active = models.BooleanField(default= True)
    flightFacilities_created_at = models.DateTimeField(auto_now_add=True)

class userFlightBookModel(models.Model):
    class Meta:
        db_table = "userFlightBook_tb"
    userFlightBook_id = models.CharField(default=None, max_length=60, primary_key=True)
    flightDetails = models.ForeignKey(flightDetailsModel, on_delete=models.CASCADE, default=None)
    userGuest = models.ForeignKey(userGuestModel, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE, default=None)
    userFlightBook_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    userFlightBook_price = models.CharField(max_length=100, default=None, blank=True, null=True)
    userFlightBook_is_active = models.BooleanField(default= True)
    userFlightBook_created_at = models.DateTimeField(auto_now_add=True)
