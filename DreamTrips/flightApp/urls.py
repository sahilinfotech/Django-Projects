from django.urls import path, include
from . import views
from  django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('', views.flightFun, name="flightPage"),
    path('filter_flights/', views.filter_flights, name='filter_flights'),
    path('-Class/<str:flightDetails_id>', views.flightclassFun, name="flightClassPage"),
    path('-Detail/<str:flightClass_id>', views.flightdetailFun, name="flightDetailPage"),


    

    
    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)