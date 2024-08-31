from django.urls import path, include
from . import views
from  django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('', views.hotelFun, name="hotelPage"),
    path('-Detail/<str:destinationHotel_id>', views.hoteldetailFun, name="hotelDetailPage"),



    

    
    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)