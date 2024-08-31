"""
URL configuration for E_Commerece project.

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
from . import views
from django.urls import path, include
from django.conf.urls.static import static
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
    path('ProductDetails/<str:id>', views.productDetailsFun, name="productDetailsPage"),
    path('add_to_wishlist/', views.addToWishlistFun, name='addToWishlistPage'),
    path('Mywishlists', views.mywishlistsFun, name="mywishlistsPage"),
    # path('remove-from-wishlist', views.removeFromWishlistFun, name='removefromwishlistPage'),
    path('remove_from_wishlist/<str:product_id>/', views.removeFromWishlistFun, name='removefromwishlistPage'),

    path('adminpanel/',include('adminPanel.urls'), name="adminpanelPage"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


