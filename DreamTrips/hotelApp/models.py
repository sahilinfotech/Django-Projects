from django.db import models
from userApp.models import *
from tourApp.models import *

from userApp.models import *
# Create your models here.

class roomTypeModel(models.Model):
    class Meta:
        db_table = "roomType_tb"
    roomType_id = models.CharField(default=None, max_length=60, primary_key=True)
    roomType_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    roomType_is_active = models.BooleanField(default= True)
    roomType_created_at = models.DateTimeField(auto_now_add=True)

class amenitiesModel(models.Model):
    class Meta:
        db_table = "amenities_tb"
    amenities_id = models.CharField(default=None, max_length=60, primary_key=True)
    amenities_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    amenities_is_active = models.BooleanField(default= True)
    amenities_created_at = models.DateTimeField(auto_now_add=True)

class activitiesModel(models.Model):
    class Meta:
        db_table = "activities_tb"
    activities_id = models.CharField(default=None, max_length=60, primary_key=True)
    activities_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    activities_is_active = models.BooleanField(default= True)
    activities_created_at = models.DateTimeField(auto_now_add=True)
    
class serviceModel(models.Model):
    class Meta:
        db_table = "service_tb"
    service_id = models.CharField(default=None, max_length=60, primary_key=True)
    service_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    service_is_active = models.BooleanField(default= True)
    service_created_at = models.DateTimeField(auto_now_add=True)
    
class destinationHotelModel(models.Model):
    class Meta:
        db_table = "destinationHotel_tb"
    destinationHotel_id = models.CharField(default=None, max_length=60, primary_key=True)
    Destinationstay = models.ForeignKey(DestinationstayModel, on_delete=models.CASCADE, default=None)
    destinationHotel_hotel_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    destinationHotel_hotel_price = models.CharField(max_length=100, default=None, blank=True, null=True)
    destinationHotel_hotel_discount = models.CharField(max_length=100, default=None, blank=True, null=True)
    destinationHotel_parking = models.BooleanField(default= False)
    destinationHotel_wifi = models.BooleanField(default= True)
    destinationHotel_eating = models.BooleanField(default= True)
    destinationHotel_cooling = models.BooleanField(default= True)
    destinationHotel_only_adults = models.BooleanField(default= False)
    destinationHotel_pet_allowed = models.BooleanField(default= False)
    destinationHotel_is_active = models.BooleanField(default= True)
    destinationHotel_created_at = models.DateTimeField(auto_now_add=True)

class destinationHotelImageModel(models.Model):
    class Meta:
        db_table = "hotel_tb"
    destinationHotelImage_id = models.CharField(default=None, max_length=60, primary_key=True)
    destinationHotel = models.ForeignKey(destinationHotelModel, on_delete=models.CASCADE, default=None)
    destinationHotelImage_image = models.ImageField(upload_to='hotel/')
    destinationHotelImage_is_active = models.BooleanField(default= True)
    destinationHotelImage_created_at = models.DateTimeField(auto_now_add=True)

class hotelRoomTypeModel(models.Model):
    class Meta:
        db_table = "hotelRoomType_tb"
    hotelRoomType_id = models.CharField(default=None, max_length=60, primary_key=True)
    destinationHotel = models.ForeignKey(destinationHotelModel, on_delete=models.CASCADE, default=None)
    roomType = models.ForeignKey(roomTypeModel, on_delete=models.CASCADE, default=None)
    hotelRoomType_is_active = models.BooleanField(default= True)
    hotelRoomType_created_at = models.DateTimeField(auto_now_add=True)

class hotelAmenitiesModel(models.Model):
    class Meta:
        db_table = "hotelAmenities_tb"
    hotelAmenities_id = models.CharField(default=None, max_length=60, primary_key=True)
    destinationHotel = models.ForeignKey(destinationHotelModel, on_delete=models.CASCADE, default=None)
    amenities = models.ForeignKey(amenitiesModel, on_delete=models.CASCADE, default=None)
    hotelAmenities_is_active = models.BooleanField(default= True)
    hotelAmenities_created_at = models.DateTimeField(auto_now_add=True)

class hotelActivitiesModel(models.Model):
    class Meta:
        db_table = "hotelActivities_tb"
    hotelActivities_id = models.CharField(default=None, max_length=60, primary_key=True)
    destinationHotel = models.ForeignKey(destinationHotelModel, on_delete=models.CASCADE, default=None)
    activities = models.ForeignKey(activitiesModel, on_delete=models.CASCADE, default=None)
    hotelActivities_is_active = models.BooleanField(default= True)
    hotelActivities_created_at = models.DateTimeField(auto_now_add=True)

class hotelServiceModel(models.Model):
    class Meta:
        db_table = "hotelService_tb"
    hotelService_id = models.CharField(default=None, max_length=60, primary_key=True)
    destinationHotel = models.ForeignKey(destinationHotelModel, on_delete=models.CASCADE, default=None)
    service = models.ForeignKey(serviceModel, on_delete=models.CASCADE, default=None)
    hotelService_is_active = models.BooleanField(default= True)
    hotelService_created_at = models.DateTimeField(auto_now_add=True)


class userGuestModel(models.Model):
    class Meta:
        db_table = 'userGuest_tb'
    userGuest_id = models.CharField(default=None, max_length=60, primary_key=True)
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE, default=None)
    userGuest_firstname = models.CharField(max_length = 30, default=None, blank=True, null=True)
    userGuest_lastname = models.CharField(max_length = 30, default=None, blank=True, null=True)
    userGuest_dateofbirth = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userGuest_gender = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userGuest_passport_number = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userGuest_passport_expire = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userGuest_nationality = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userGuest_created_at = models.DateTimeField(auto_now_add=True)

class userHotelModel(models.Model):
    class Meta:
        db_table = ' userHotel_tb'
    userHotel_id = models.CharField(default=None, max_length=60, primary_key=True)
    userGuest = models.ForeignKey(userGuestModel, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE, default=None)
    destinationHotel = models.ForeignKey(destinationHotelModel, on_delete=models.CASCADE, default=None)
    userHotel_check_in_date = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userHotel_check_out_date = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userHotel_check_in_period = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userHotel_check_out_period = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userHotel_totallenghtostay = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userHotel_totalmembers = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userHotel_nationality = models.CharField(max_length = 50, default=None, blank=True, null=True)
    userHotel_created_at = models.DateTimeField(auto_now_add=True)


