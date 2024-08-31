from django.shortcuts import render, redirect
from E_Commerece import *
from E_Commerece.models import *
from adminPanel.models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage  #for File storage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
import json
import random
import string
import os
import io
from django.conf import settings
from E_Commerece.emailsend import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.


media_path = "../../../"

def generate_random_string():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(10))

def signUpFun(request):
    try:
        if request.method == "POST":
            
            user_fname_ = request.POST['userFirstName']
            user_lname_ = request.POST['userLastName']
            user_mobile_num_ = request.POST['userPhoneNo']
            user_username_ = request.POST['userName']
            user_email_ = request.POST['userEmail']
            user_password_ = request.POST['userPassword']                    
                    
            if len(user_fname_) <= 0:
                
                error = "Please Enter First Name !!"
                return render(request, 'signup.html', {"error":error, "flag" : 0})

            if not user_fname_.isalpha():

                error="Please enter a valid First Name (only text characters are filterowed)"
                return render(request, 'signup.html', {"error":error, "flag" : 0})
            
            if len(user_lname_) <= 0:

                error="Please Enter Last Name !!"
                return render(request, 'signup.html', {"error":error, "flag" : 0})

            if not user_lname_.isalpha():

                error="Please enter a valid Last Name (only text characters are filterowed)"
                return render(request, 'signup.html', {"error":error, "flag" : 0})
            
            if len(user_mobile_num_) <= 0:

                error="Please Enter PhoneNo. !!"
                return redirect(signUpFun, error="Please Enter PhoneNo. !!")
            
            if not user_mobile_num_.isdigit():

                error="Please enter a valid Phone No. (only digits are filterowed)"
                return render(request, 'signup.html', {"error":error, "flag" : 0})
            
            if len(user_username_) <= 0:

                error="Please Enter User Name !!"
                return render(request, 'signup.html', {"error":error, "flag" : 0})

            if len(user_email_) <= 0:

                error="Please Enter Email !!"
                return render(request, 'signup.html', {"error":error, "flag" : 0})
            
            try:

                validate_email(user_email_)

            except ValidationError:

                error="Please enter a valid email address!"
                return render(request, 'signup.html', {"error":error, "flag" : 0})
            
            if userModel.objects.filter(user_email=user_email_).exists():

                error="User Email is already existed!!"
                return render(request, 'signup.html', {"error":error, "flag" : 0})
            
            if len(user_password_) <= 0:

                error="Please Enter User Password !!"
                return render(request, 'signup.html', {"error":error, "flag" : 0})
            

            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            uniqueID = "ProductAR_" + randomstr
            
            






            user_email_ = user_email_.lower()
            Useradddata = userModel(
                user_id = uniqueID,
                user_fname = user_fname_,
                user_lname = user_lname_,
                user_mobile_num = user_mobile_num_,
                user_username = user_username_,
                user_email = user_email_,
                # user_password = user_password_,
                user_password = make_password(user_password_,salt=randomstr, hasher='argon2')
            )

            Useradddata.save()
                        
            if Useradddata.user_id:
                
                randomstr = ''.join(random.choices(string.digits, k=6))
                request.session['loginotp'] = randomstr
                request.session['otp'] = None
                email_status = mailSend(request, user_email_, randomstr)

                return redirect(otp)
                

            else:

                error="Something is wrong!!"
                return render(request, 'signup.html', {"error":error, "flag" : 0})

        return render(request, 'signup.html', {"error":"", "flag" : 0})

    except Exception as e:
        print("Error", e)
        return render(request, '404_Page.html')

def loginFun(request):
        messages = ''
        if "userinfo" in request.session:
            if request.session["userinfo"] != None:
                userDetails = request.session["userinfo"]
                return redirect(productFun)
            elif request.session["userinfo"] == None:
                messages = ''
                if request.method == 'POST':
                    userEmail = request.POST['userEmail']
                    password = request.POST['password']
                    if userModel.objects.using("default").filter(user_email=userEmail).exists():
                        userdetails = userModel.objects.using("default").get(user_email=userEmail)
                    
                        check_pwd = check_password(password, userdetails.user_password)  # Assign check_pwd here
                        if check_pwd:  # Now check_pwd is assigned before using it
                            request.session["userinfo"] = {"username_loggged": userEmail, "user_id": userdetails.user_id }
                            request.session["loginotp"]=None
                            return redirect(productFun)
                        else:
                            messages = 'Password is Invalid'
                            return render(request, "login.html", {"message": messages, "flag" : 0})
                        
                        
                    else:
                        messages = 'User Email is invalid'
                        return render(request, "login.html", {"message": messages, "flag" : 0})
                return render(request, "login.html", {"message": messages, "flag" : 0})
        else:
            messages=''
            request.session["userinfo"] = None
            return render(request, "login.html", {"message": messages, "flag" : 0})

def logoutFun(request):
    
    userDetails = request.session["userinfo"]
    request.session["userinfo"] = None
    request.session["loginotp"]=None
    request.session["otp"]=None
    return redirect(loginFun)
    
def forgotpasswordFun(request):
    if request.method == 'POST':
        user_email = request.POST.get('useremail') 
        
        if userModel.objects.filter(user_email=user_email).exists():
            randomstr = ''.join(random.choices(string.digits, k=6))  
            request.session['otp'] = randomstr
            request.session['user_email'] = user_email
            
            email_status = mailSend(request, user_email, randomstr)

            return redirect(otp)
            
        else:
            error = "Email address not found."
            return render(request, 'forgot_password.html', {"error":error,"flag": 0})
    return render(request, 'forgot_password.html', {"flag": 0})

def otp(request):
    if request.method == 'POST':
        user_otp = request.POST['userotp']
        # Retrieve OTP from the session
        if request.session['otp'] is not None:
            otp = request.session['otp']         
            if user_otp == otp:
                error="Please Enter Valid OTP !!"
                return render(request, 'new_password.html', {"error":error, "flag" : 0})
            else:
                error = "Invalid OTP. Please try again."
                return render(request, 'otp.html', {"error": error, "flag": 0})
        if request.session['loginotp'] is not None:
            loginotp = request.session['loginotp']
            
            # Check if user-entered OTP matches the login OTP stored in the session
            if user_otp == loginotp:
                error = "Please Enter Valid OTP !!"
                return render(request, 'login.html', {"error": error, "flag": 0})
            else:
                error = "Invalid OTP. Please try again."
                return render(request, 'otp.html', {"error": error, "flag": 0})
    
    return render(request, 'otp.html', {"flag": 0})      

def newpassword(request):
    if request.method == 'POST':
        user_new_password = request.POST.get('usernewpassword')

        if 'user_email' in request.session:
            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            user_email = request.session['user_email']
            if userModel.objects.filter(user_email=user_email).exists():
                user = userModel.objects.get(user_email=user_email)
                user.user_password = make_password(user_new_password,salt=randomstr, hasher='argon2')
                user.save()
                request.session["otp"]=None
                return redirect(loginFun)  
            else:
                error = "Email address not found."
                return render(request, 'new_password.html', {"error":error,"flag" : 0}) 
        else:
            error = "User email not found in session."
            return render(request, 'new_password.html', {"error":error,"flag" : 0})
           


    return render(request, 'new_password.html', {"flag" : 0})
  
def productFun(request):
    context = {
        "optionClass" : "others-option"      
    }
    
    if request.session["userinfo"] != None:
        if "userinfo" in request.session:
            userDetails = request.session["userinfo"]
            
            Productdata = ProductModel.objects.filter(Product_is_active=True)


        else:
            return redirect(loginFun)
        return render(request, 'Product.html',{"Productdata":Productdata,"context":context,"userDetails": userDetails, "flag" : 1})
    else:
        return redirect(loginFun)
    
def productDetailsFun(request,id):
    context = {
    "optionClass" : "others-option",   
    }
    
    if request.session["userinfo"] != None:
        if "userinfo" in request.session:
            userDetails = request.session["userinfo"]
            productdata = ProductModel.objects.get(pk=id)
            request.session["selected_product_id"] = productdata.id
            print(productdata.Product_price)
            Productdetaildata = ProductdetailModel.objects.filter(Product=productdata).filter(Productdetail_is_active = True).values()
        else:
            return redirect(loginFun)
        return render(request, 'ProductDetails.html',{"productdata":productdata,"Productdetaildata":Productdetaildata,"context":context,"userDetails": userDetails, "flag" : 1})
    else:
        return redirect(loginFun)

def addToWishlistFun(request):
    context = {
    "optionClass" : "others-option",   
    }
    if request.session.get("userinfo"):
        userDetails = request.session["userinfo"]
        user_id = userDetails['user_id']
        selected_product_id = request.session.get('selected_product_id')
        
        if selected_product_id:
            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            uniqueID = "mywishlist_" + randomstr

            mywishlistsdata = wishlistModel(
                wishlist_id=uniqueID,
                wishlist_user=user_id,
                wishlist_product=selected_product_id,
            )
            mywishlistsdata.save()

        return redirect(mywishlistsFun)
    else:
        return redirect(loginFun)
    
def mywishlistsFun(request):
    context = {
        "optionClass": "others-option",
    }
    if request.session.get("userinfo"):
        userDetails = request.session["userinfo"]
        user_id = userDetails['user_id']
        
        wishlist_items = wishlistModel.objects.filter(wishlist_user=user_id)

        productdetailfetchdata = []
        for item in wishlist_items:
            productfetchdata = ProductModel.objects.get(id=item.wishlist_product)
            productdetails = ProductdetailModel.objects.filter(Product=productfetchdata)
            for detail in productdetails:
                productdetailfetchdata.append({
                    'Product': productfetchdata,
                    'Productdetail_description': detail.Productdetail_description,
                    'Productdetail_colour': detail.Productdetail_colour,
                    'Productdetail_type': detail.Productdetail_type,
                    'Productdetail_is_active': detail.Productdetail_is_active,
                })
        
        return render(request, 'my_wishlists.html', {
            "productdetailfetchdata": productdetailfetchdata,
            "context": context,
            "userDetails": userDetails,
            "flag": 1
        })
    else:
        return redirect(loginFun)

def removeFromWishlistFun(request, product_id):
    if request.session.get("userinfo"):
        userDetails = request.session["userinfo"]
        user_id = userDetails['user_id']
        
        wishlist_item = wishlistModel.objects.filter(wishlist_user=user_id, wishlist_product=product_id).first()
        if wishlist_item:
            wishlist_item.delete()
            request.session["selected_product_id"] = None
        return redirect(mywishlistsFun)
    
    else:
        return redirect(loginFun)