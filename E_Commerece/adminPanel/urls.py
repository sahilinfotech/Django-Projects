from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.dashboardAdmin, name="adminDashboardPage"),
    path('Product_Add',views.productregisterFun, name="productAddPage"),
    path('Product_View', views.productviewFun, name="productViewPage"),
    path('Product_Fetch', views.productfetchFun, name="productFetchPage"),
    path('Product_Edit', views.producteditFun, name="productEditPage"),
    path('Product_Delete', views.productdeleteFun, name="productDeletePage"),

    path('Productdetail_Add',views.productdetailregisterFun, name="productdetailAddPage"),
    path('Productdetail_View', views.productdetailviewFun, name="productdetailViewPage"),
    path('Productdetail_Fetch', views.productdetailfetchFun, name="productdetailFetchPage"),
    path('Productdetail_Edit', views.productdetaileditFun, name="productdetailEditPage"),
    path('Productdetail_Delete', views.productdetaildeleteFun, name="productdetailDeletePage"),
    
	]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

