"""
URL configuration for ProductAR project.

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
    path('', views.loginFun, name="loginPage"),
    path('SignUp', views.signUpFun, name="signUpPage"),
    path('logout', views.logoutFun, name='LogoutPage'),
    path('forgot-password', views.forgotpasswordFun, name='forgotpasswordPage'),
    path('otp', views.otp, name='otppage'),
    path('newpassword', views.newpassword, name='newpasswordpage'),
    path('Product', views.productFun, name="productPage"),
    path('ProductDetails', views.productDetailsFun, name="productDetailsPage"),
    path('Customize', views.customizeFun, name="customizePage"),
    path('CustomizeView', views.customizeViewFun, name="customizeViewPage"),
    path('Customize_ViewDetails/<str:customize_id>', views.customizeViewDetailsFun, name="customizeViewDetailsPage"),
    path('Customize_Delete/<str:customize_id>', views.customizeDeleteFun, name="customizeDeletePage"),

    path('uploadVideo', views.upload_video, name="uploadVideoPage"),
    path('uploadVideo_Fetch/<str:customize_id>', views.uploadvideoFetchFun, name="uploadVideoFetchPage"),
    path('uploadVideo_Edit', views.uploadvideoEditFun, name="uploadVideoEditPage"),

    

    
    # path('adminpanel/', include('insightsmith_adminpanel.urls'), name="insightsmith_adminpanelPage"),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
