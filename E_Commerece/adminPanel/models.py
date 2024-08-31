from django.db import models

# Create your models here.

class ProductModel(models.Model):
    Product_name = models.CharField(max_length = 100, default=None, blank=True, null=True)
    Product_price = models.CharField(max_length = 100, default=None, blank=True, null=True)
    Product_image = models.TextField(default=None, blank=True, null=True)
    Product_is_active = models.BooleanField(default=True)
    Product_created_at = models.DateTimeField(auto_now_add = True)
    Product_created_at_update = models.CharField(default = "None", blank = True, null = True)



class ProductdetailModel(models.Model):
    Product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, default=None)
    Productdetail_description = models.TextField(default=None, blank=True, null=True)
    Productdetail_type = models.CharField(max_length = 100, default=None, blank=True, null=True)
    Productdetail_colour = models.CharField(max_length = 100, default=None, blank=True, null=True)
    Productdetail_is_active = models.BooleanField(default=True, blank=True, null=True)
    Productdetail_created_at = models.DateTimeField(auto_now_add = True)
    Productdetail_created_at_update = models.CharField(default = "None", blank = True, null = True)


