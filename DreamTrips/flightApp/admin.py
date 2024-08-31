from django.contrib import admin
from flightApp.models import *

# Register your models here.

admin.site.register(flightModel)
admin.site.register(flightFacilitiesModel)
admin.site.register(flightClassModel)
admin.site.register(flightDetailsModel)
admin.site.register(userFlightBookModel)
