from django.db import models
from userApp.models import *
# Create your models here.

class BillingModel(models.Model):
    class Meta:
        db_table = "Billing_tb"
    Billing_id = models.CharField(default=None, max_length=60, primary_key=True)
    Billing_user = models.CharField(max_length=100, default=None, blank=True, null=True)
    Billing_destination = models.CharField(max_length=100, default=None, blank=True, null=True)
    Billing_flight = models.CharField(max_length=100, default=None, blank=True, null=True)
    Billing_hotel = models.CharField(max_length=100, default=None, blank=True, null=True)
    Billing_created_at = models.DateTimeField(auto_now_add=True)

    
class userBillingModel(models.Model):
    class Meta:
        db_table = "userBilling_tb"
    userBilling_id = models.CharField(default=None, max_length=60, primary_key=True)
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE, default=None)
    userBilling_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    userBilling_poastal_code = models.CharField(max_length=100, default=None, blank=True, null=True)
    userBilling_city = models.CharField(max_length=100, default=None, blank=True, null=True)
    userBilling_country = models.CharField(max_length=100, default=None, blank=True, null=True)
    userBilling_phoneno = models.CharField(max_length=100, default=None, blank=True, null=True)
    userBilling_email = models.CharField(max_length=100, default=None, blank=True, null=True)
    userBilling_price = models.CharField(max_length=100, default=None, blank=True, null=True)
    userBilling_is_active = models.BooleanField(default= True)
    userBilling_created_at = models.DateTimeField(auto_now_add=True)

class bookingSuccessfulModel(models.Model):
    class Meta:
        db_table = "bookingSuccessful_tb"
    bookingSuccessful_id = models.CharField(default=None, max_length=60, primary_key=True)
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE, default=None)
    bookingSuccessful_firstname = models.CharField(max_length=100, default=None, blank=True, null=True)
    bookingSuccessful_lastname = models.CharField(max_length=100, default=None, blank=True, null=True)
    bookingSuccessful_order_invoice = models.CharField(max_length=100, default=None, blank=True, null=True)
    bookingSuccessful_total_amount = models.CharField(max_length=100, default=None, blank=True, null=True)
    bookingSuccessful_payment_mode = models.CharField(max_length=100, default=None, blank=True, null=True)
    bookingSuccessful_phoneno = models.CharField(max_length=100, default=None, blank=True, null=True)
    bookingSuccessful_email = models.CharField(max_length=100, default=None, blank=True, null=True)
    bookingSuccessful_account_number = models.CharField(max_length=100, default=None, blank=True, null=True)
    bookingSuccessful_is_active = models.BooleanField(default= True)
    bookingSuccessful_created_at = models.DateTimeField(auto_now_add=True)