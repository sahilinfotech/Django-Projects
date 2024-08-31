# Create your models here.
from django.db import models

class DestinationModel(models.Model):
    class Meta:
        db_table = "Destination_tb"
    Destination_id = models.CharField(default=None, max_length=60, primary_key=True)
    Destination_place = models.CharField(max_length=100, default=None, blank=True, null=True)
    Destinationstay_image = models.ImageField(upload_to='destination/')
    Destination_is_active = models.BooleanField(default= True)
    Destination_created_at = models.DateTimeField(auto_now_add=True)

class UserselectdestinationModel(models.Model):
    class Meta:
        db_table = "Userselectdestination_tb"
    Userselectdestination_id = models.CharField(default=None, max_length=60, primary_key=True)
    Destination = models.ForeignKey(DestinationModel, on_delete=models.CASCADE, default=None)
    Userselectdestination_stay_period = models.CharField(max_length=100, default=None, blank=True, null=True)
    Userselectdestination_is_active = models.BooleanField(default= True)
    Userselectdestination_created_at = models.DateTimeField(auto_now_add=True)

class DestinationstayModel(models.Model):
    class Meta:
        db_table = "Destinationstay_tb"
    Destinationstay_id = models.CharField(default=None, max_length=60, primary_key=True)
    Destination = models.ForeignKey(DestinationModel, on_delete=models.CASCADE, default=None)
    Destinationstay_place_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Destinationstay_highligh_1 = models.TextField(default=None, blank=True, null=True)
    Destinationstay_highligh_2 = models.TextField(default=None, blank=True, null=True)
    Destinationstay_highligh_3 = models.TextField(default=None, blank=True, null=True)
    Destinationstay_highligh_4 = models.TextField(default=None, blank=True, null=True)
    Destinationstay_highligh_5 = models.TextField(default=None, blank=True, null=True)
    Destinationstay_highligh_6 = models.TextField(default=None, blank=True, null=True)
    Destinationstay_meal_plan = models.BooleanField(default= True)
    Destinationstay_services = models.BooleanField(default= True)
    Destinationstay_inter_city_transfer = models.BooleanField(default= False)
    Destinationstay_charges = models.BooleanField(default= True)
    Destinationstay_lunch = models.BooleanField(default= True)
    Destinationstay_parking_fees = models.BooleanField(default= False)
    Destinationstay_breakfast = models.BooleanField(default= True)
    Destinationstay_stationorairpot_pickanddrop = models.BooleanField(default= False)
    Destinationstay_personal_travel = models.BooleanField(default= False)
    Destinationstay_dinner = models.BooleanField(default= True)
    Destinationstay_price = models.CharField(max_length=100, default=None, blank=True, null=True)
    Destinationstay_image_1 = models.ImageField(upload_to='destination/')
    Destinationstay_image_2 = models.ImageField(upload_to='destination/')
    Destinationstay_image_3 = models.ImageField(upload_to='destination/')
    Destinationstay_is_active = models.BooleanField(default= True)
    Destinationstay_created_at = models.DateTimeField(auto_now_add=True)
