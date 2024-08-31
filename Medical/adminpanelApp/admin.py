from django.contrib import admin
from adminpanelApp.models import *
# Register your models here.

admin.site.register(medicineModel)
admin.site.register(sellmedicineModel)
admin.site.register(patientdetailModel)
admin.site.register(patientmedicineModel)
admin.site.register(userModel)

