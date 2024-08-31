from django.db import models


class contactUsModel(models.Model):
    class Meta:
        db_table = "contactUsmodel_tb"
    contactUs_id = models.CharField(default=None, max_length=60, primary_key=True)
    contactUs_name = models.CharField(max_length = 100, default=None, blank=True, null=True)
    contactUs_email = models.CharField(max_length = 100, default=None, blank=True, null=True)
    contactUs_phone = models.CharField(max_length = 100, default=None, blank=True, null=True)
    contactUs_subject = models.CharField(max_length = 250, default=None, blank=True, null=True)
    contactUs_query = models.TextField(default=None, blank=True, null=True)
    contactUs_created_at = models.DateTimeField(auto_now_add=True)
