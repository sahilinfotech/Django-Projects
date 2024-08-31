from django.urls import path, include
from . import views
from  django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

	path('map', views.indexFun, name="indexPage"),
    
	path('', views.index, name='index'),
    path('get_location/', views.get_location, name='get_location'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

