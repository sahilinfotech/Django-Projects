from django.db import models

# Create your models here.

class SignupModel(models.Model):
    class Meta:
        db_table = 'Signup_tb'
    user_id = models.CharField(default=None, max_length=60, primary_key=True)
    user_firstname = models.CharField(max_length = 30, default=None, blank=True, null=True)
    user_lastname = models.CharField(max_length = 30, default=None, blank=True, null=True)
    user_email = models.CharField(max_length = 100, default=None, blank=True, null=True)
    user_password = models.CharField(max_length = 250, default=None, blank=True, null=True)
    user_username = models.CharField(max_length = 100, default=None, blank=True, null=True)
    user_mobile = models.CharField(max_length = 60, default=None, blank=True, null=True)
    user_dateofbirth = models.CharField(max_length = 50, default=None, blank=True, null=True)
    user_gender = models.CharField(max_length = 50, default=None, blank=True, null=True)
    user_city = models.CharField(max_length = 50, default=None, blank=True, null=True)
    user_state = models.CharField(max_length = 50, default=None, blank=True, null=True)
    user_country = models.CharField(max_length = 50, default=None, blank=True, null=True)
    user_image = models.TextField(default=None, blank=True, null=True)
    user_is_loggin = models.BooleanField(default= True)
    user_created_at = models.DateTimeField(auto_now_add=True)
    user_created_at_update = models.CharField(max_length=100, default=None, blank=True, null=True)
