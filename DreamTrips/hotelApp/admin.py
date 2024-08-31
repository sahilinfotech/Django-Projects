from django.contrib import admin
from hotelApp.models import *

# Register your models here.

admin.site.register(roomTypeModel)
admin.site.register(amenitiesModel)
admin.site.register(activitiesModel)
admin.site.register(serviceModel)
admin.site.register(destinationHotelModel)
admin.site.register(hotelRoomTypeModel)
admin.site.register(hotelAmenitiesModel)
admin.site.register(hotelActivitiesModel)
admin.site.register(hotelServiceModel)
admin.site.register(userGuestModel)
admin.site.register(userHotelModel)
admin.site.register(destinationHotelImageModel)