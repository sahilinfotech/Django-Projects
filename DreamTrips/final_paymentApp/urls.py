from django.urls import path, include
from . import views
from  django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('', views.bookingFun, name="bookingPage"),
    path('-Detail', views.bookingdetailFun, name="bookingDetailPage"),
    path('-Payment', views.bookingpaymentFun, name="bookingPaymentPage"),
    path('-Success', views.bookingsuccessFun, name="bookingSuccessPage"),
    # path('save_booking/', views.save_booking, name='save_booking'),


    

    
    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)