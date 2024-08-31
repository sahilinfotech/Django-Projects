from django.urls import path, include
from . import views
from  django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('Login', views.loginFun, name="loginPage"),
    path('SignUp', views.signupFun, name="signupPage"),
    path('logout', views.logoutFun, name='LogoutPage'),
    path('forgot-password', views.forgotpasswordFun, name='forgotpasswordPage'),
    path('otp', views.otp, name='otppage'),
    path('newpassword', views.newpassword, name='newpasswordpage'),
    path('Mybooking', views.mybookingFun, name="mybookingPage"),
    path('Mywishlists', views.mywishlistsFun, name="mywishlistsPage"),
    path('Myprofile', views.myprofileFun, name="myprofilePage"),
    path('Myprofilepassword', views.myprofilepasswordFun, name="myprofilepasswordPage"),



    

    
    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

