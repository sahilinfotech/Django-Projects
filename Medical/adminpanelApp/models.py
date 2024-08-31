from django.db import models

class userModel(models.Model):
    class Meta:
        db_table = 'adminuser_tb'
    user_id = models.CharField(default="None", max_length=60, primary_key=True)
    user_fname = models.CharField(max_length = 30, default="None", blank=True, null=True)
    user_lname = models.CharField(max_length = 30, default="None", blank=True, null=True)
    user_gender = models.CharField(max_length=10, default="None",null=True, blank=True)
    user_mobile_num = models.CharField(max_length = 15, default="None", blank=True, null=True)
    user_username = models.CharField(max_length = 100, default="None", blank=True, null=True)
    user_email = models.CharField(max_length = 100, default="None", blank=True, null=True)
    user_password = models.CharField(max_length = 30, default="None", blank=True, null=True)
    user_emp_type = models.CharField(max_length = 30, default="None", blank=True, null=True)
    user_is_active = models.CharField(default="None")
    user_created_at = models.DateTimeField(auto_now_add=True)
    user_created_at_update = models.CharField(max_length=100, default="None", blank=True, null=True)

class medicineModel(models.Model):
    class Meta:
        db_table = "medicinemodel_tb"
    medicine_id = models.CharField(default=None, max_length= 60, primary_key=True)
    medicine_name = models.CharField(max_length = 100, default = None, blank = True, null = True)
    medicine_price = models.CharField(max_length = 100, default = None, blank = True, null = True)
    medicine_quantity = models.CharField(max_length = 100, default = None, blank = True, null = True)
    medicine_remember_quantity = models.CharField(max_length = 100, default = None, blank = True, null = True)
    medicine_mfg_date = models.CharField(max_length = 100, default = None, blank = True, null = True)
    medicine_expiry_date = models.CharField(max_length = 100, default = None, blank = True, null = True)
    medicine_mg = models.CharField(max_length = 100, default = None, blank = True, null = True)
    medicine_barcode = models.ImageField(upload_to='barcodes/', default=None, blank=True, null=True)
    medicine_is_active = models.BooleanField(default= True)
    medicine_created_at = models.DateTimeField(auto_now_add = True)
    medicine_created_at_update = models.CharField(max_length = 100, default = None, blank = True, null = True)

class sellmedicineModel(models.Model):
    class Meta:
        db_table = "sellmedicinemodel_tb"
    sellmedicine_id = models.CharField(default=None, max_length= 60, primary_key=True)
    medicine = models.ForeignKey(medicineModel, on_delete=models.CASCADE, default=None)
    sellmedicine_name = models.CharField(max_length = 100, default = None, blank = True, null = True)
    sellmedicine_price = models.CharField(max_length = 100, default = None, blank = True, null = True)
    sellmedicine_quantity = models.CharField(max_length = 100, default = None, blank = True, null = True)
    sellmedicine_remember_quantity = models.CharField(max_length = 100, default = None, blank = True, null = True)
    sellmedicine_is_active = models.BooleanField(default= True)
    sellmedicine_created_at = models.DateTimeField(auto_now_add = True)
    sellmedicine_created_at_update = models.CharField(max_length = 100, default = None, blank = True, null = True)

class patientdetailModel(models.Model):
    class Meta:
        db_table = "patientdetailmodel_tb"
    patientdetail_id = models.CharField(default=None, max_length= 60, primary_key=True)
    patientdetail_name = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientdetail_doctor_name = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientdetail_diseases_description = models.TextField(default=None, blank=True, null=True)
    patientdetail_mobile_no = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientdetail_totalprice = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientdetail_is_active = models.BooleanField(default= True)
    patientdetail_created_at = models.DateTimeField(auto_now_add = True)

class patientmedicineModel(models.Model):
    class Meta:
        db_table = "patientmedicinemodel_tb"
    patientmedicine_id = models.CharField(default=None, max_length= 60, primary_key=True)
    medicine = models.ForeignKey(medicineModel, on_delete=models.CASCADE, default=None)
    patientdetail = models.ForeignKey(patientdetailModel, on_delete=models.CASCADE, default=None)
    patientmedicine_medicine_name = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientmedicine_mg = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientmedicine_price = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientmedicine_quantity = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientmedicine_remember_quantity = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientmedicine_totalprice = models.CharField(max_length = 100, default = None, blank = True, null = True)
    patientmedicine_is_active = models.BooleanField(default= True)
    patientmedicine_created_at = models.DateTimeField(auto_now_add = True)
    patientmedicine_created_at_update = models.CharField(max_length = 100, default = None, blank = True, null = True)
