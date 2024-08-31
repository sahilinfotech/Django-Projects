from django.urls import path, include
from . import views
from  django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('', views.dashboardFun, name="dashboardPage"),
    # path('', views.loginFun, name='userLoginPage'),
    # path('logout', views.logoutFun, name='userLogoutPage'),
    
    # # path('forgot-password', views.forgot_password, name='forgot_password'),
    # # path('otp', views.otp, name='otppage'),
    # # path('newpassword', views.newpassword, name='newpasswordpage'),
    
	# About Page
	path('medicine_Register', views.medicineRegisterFun, name="medicineAddPage"),
	path('medicine_View', views.medicineViewFun, name="medicineViewPage"),
    path('medicine_Viewdetails/<str:medicine_id>',views.medicineViewdetailsFun,name="medicineViewdetailsPage"),
	path('medicine_Fetch/<str:medicine_id>', views.medicineFetchFun, name="medicineFetchPage"),
	path('medicine_Edit', views.medicineEditFun, name="medicineEditPage"),
	path('medicine_Delete/<str:medicine_id>', views.medicineDeleteFun, name="medicineDeletePage"),

	path('medicine_datafetch/<str:medicine_name>/', views.medicinedatafetchFun, name='medicinedatafetchPage'),
	# path('medicine_datafetch/<str:medicine_name>/<str:medicine_mg>/', views.medicinedatafetchFunWithMg, name='medicinedatafetchWithMg'),

	
	path('sellmedicine_Register', views.sellmedicineRegisterFun, name="sellmedicineAddPage"),
	path('sellmedicine_View', views.sellmedicineViewFun, name="sellmedicineViewPage"),
    path('sellmedicine_Viewdetails/<str:sellmedicine_id>',views.sellmedicineViewdetailsFun,name="sellmedicineViewdetailsPage"),
	path('sellmedicine_Fetch/<str:sellmedicine_id>', views.sellmedicineFetchFun, name="sellmedicineFetchPage"),
	path('sellmedicine_Edit', views.sellmedicineEditFun, name="sellmedicineEditPage"),
	path('sellmedicine_Delete/<str:sellmedicine_id>', views.sellmedicineDeleteFun, name="sellmedicineDeletePage"),
    
	path('patientdetail_Register', views.patientdetailRegisterFun, name="patientdetailAddPage"),
	path('patientdetail_View', views.patientdetailViewFun, name="patientdetailViewPage"),
    path('patientdetail_Viewdetails/<str:patientdetail_id>',views.patientdetailViewdetailsFun,name="patientdetailViewdetailsPage"),
	path('patientdetail_Edit', views.patientdetailEditFun, name="patientdetailEditPage"),
	path('patientdetail_Delete/<str:patientdetail_id>', views.patientdetailDeleteFun, name="patientdetailDeletePage"),

	path('outofstock_View', views.outofstockViewFun, name="outofstockViewPage"),
	path('expirymedicine_View', views.expirymedicineViewFun, name="expirymedicineViewPage"),

	path('patientmedicine_Register', views.patientmedicineRegisterFun, name="patientmedicineAddPage"),
    path('patientmedicine_Edit/<str:patientmedicine_id>', views.patientmedicineEditFun, name="patientmedicineEditPage"),
	path('patientmedicine_Delete/<str:patientmedicine_id>', views.patientmedicineDeleteFun, name="patientmedicineDeletePage"),
	path('patient_bill', views.patient_bill, name="patientbillPage"),
    
    
    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

