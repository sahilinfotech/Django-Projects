from django.urls import path, include
from . import views
from  django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

	path('Demo', views.demoFun, name="demoPage"),

    path('Dashboard', views.indexRegisterFun, name="indexAddPage"),
    # path('', views.loginFun, name='userLoginPage'),

    path('bangalow_Register', views.bangalowRegisterFun, name="bangalowAddPage"),
	path('bangalow_View', views.bangalowViewFun, name="bangalowViewPage"),
    path('bangalow_Viewdetails/<str:bangalow_id>',views.bangalowViewdetailsFun,name="bangalowViewdetailsPage"),
	path('bangalow_Fetch/<str:bangalow_id>', views.bangalowFetchFun, name="bangalowFetchPage"),
	path('bangalow_Edit', views.bangalowEditFun, name="bangalowEditPage"),
	path('bangalow_Delete/<str:bangalow_id>', views.bangalowDeleteFun, name="bangalowDeletePage"),
    
	path('visitor_Register', views.visitorRegisterFun, name="visitorAddPage"),
	path('visitor_View', views.visitorViewFun, name="visitorViewPage"),
    path('visitor_Viewdetails/<str:visitor_id>',views.visitorViewdetailsFun,name="visitorViewdetailsPage"),
	path('visitor_Fetch/<str:visitor_id>', views.visitorFetchFun, name="visitorFetchPage"),
	path('visitor_Edit', views.visitorEditFun, name="visitorEditPage"),
	path('visitor_Delete/<str:visitor_id>', views.visitorDeleteFun, name="visitorDeletePage"),
    
	path('client_datafetch/<str:visitor_id>/', views.clientdatafetchFun, name='clientdatafetchPage'),
	path('client_Register', views.clientRegisterFun, name="clientAddPage"),
	path('client_View', views.clientViewFun, name="clientViewPage"),
    path('client_Viewdetails/<str:client_id>',views.clientViewdetailsFun,name="clientViewdetailsPage"),
	path('client_Fetch/<str:client_id>', views.clientFetchFun, name="clientFetchPage"),
	path('client_Edit', views.clientEditFun, name="clientEditPage"),
	path('client_Delete/<str:client_id>', views.clientDeleteFun, name="clientDeletePage"),
    
	path('moneyManagement_datafetch/<str:client_id>/', views.moneyManagementdatafetchFun, name='moneyManagementdatafetchPage'),
	path('moneyManagement_tablefetch/<str:client_id>/', views.moneyManagementtablefetchFun, name='moneyManagementtablefetchPage'),
	path('moneyManagement_Register', views.moneyManagementRegisterFun, name="moneyManagementAddPage"),
	path('moneyManagement_View', views.moneyManagementViewFun, name="moneyManagementViewPage"),
	path('moneyManagement_Viewdetails/<str:moneyManagement_id>',views.moneyManagementViewdetailsFun,name="moneyManagementViewdetailsPage"),
	path('moneyManagement_Fetch/<str:moneyManagement_id>', views.moneyManagementFetchFun, name="moneyManagementFetchPage"),
	path('moneyManagement_Edit', views.moneyManagementEditFun, name="moneyManagementEditPage"),
	path('moneyManagement_Delete/<str:moneyManagement_id>', views.moneyManagementDeleteFun, name="moneyManagementDeletePage"),
   
	path('resume_Register', views.resumeRegisterFun, name="resumeAddPage"),
    path('resume_View', views.resumeViewFun, name="resumeViewPage"),
    path('resume_Fetch', views.resumeFetchFun, name="resumeFetchPage"),
	path('resume_Edit', views.resumeEditFun, name="resumeEditPage"),
	path('resume_Delete', views.resumeDeleteFun, name="resumeDeletePage"),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

