"""
URL configuration for DreamTrips project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from  django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexFun, name="indexPage"),
    path('Contact', views.contactUsFun, name="contactUsPage"),
    path('Contact_Add', views.contactUsRegisterFun, name="contactUsAddPage"),
    path('Help', views.helpCenterFun, name="helpCenterPage"),
    path('User/', include('userApp.urls'), name="user_AppPage"),
    path('Tours', include('tourApp.urls'), name="tourAppPage"),
    path('Hotels', include('hotelApp.urls'), name="hotelAppPage"),
    path('Flights', include('flightApp.urls'), name="flightAppPage"),
    path('Booking', include('final_paymentApp.urls'), name='finalPaymentAppPage'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
