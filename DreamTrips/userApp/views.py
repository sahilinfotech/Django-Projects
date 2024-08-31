
from django.shortcuts import render, redirect
from DreamTrips import *
from final_paymentApp.models import *
from tourApp.models import *
from flightApp.models import *
from hotelApp.models import *
from DreamTrips.emailsend import *
from DreamTrips.google_info import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage  #for File storage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
import random
import string
import os
import io
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.
def signupFun(request):
    # try:
    if request.method == "POST":
        
        user_firstname_ = request.POST['userFirstName']
        user_lastname_ = request.POST['userLastName']
        user_username_ = request.POST['userName']
        user_email_ = request.POST['userEmail']
        user_password_ = request.POST['userPassword']
        user_image_ = request.FILES.get('userImage', False)
            
                
        if len(user_firstname_) <= 0:
            
            error = "Please Enter First Name !!"
            return render(request, 'signup.html', {"error":error, "flag" : 0})

        if not user_firstname_.isalpha():

            error="Please enter a valid First Name (only text characters are filterowed)"
            return render(request, 'signup.html', {"error":error, "flag" : 0})
        
        if len(user_lastname_) <= 0:

            error="Please Enter Last Name !!"
            return render(request, 'signup.html', {"error":error, "flag" : 0})

        if not user_lastname_.isalpha():

            error="Please enter a valid Last Name (only text characters are filterowed)"
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
        
        if SignupModel.objects.filter(user_email=user_email_).exists():

            error="User Email is already existed!!"
            return render(request, 'signup.html', {"error":error, "flag" : 0})
        
        if len(user_password_) <= 0:

            error="Please Enter User Password !!"
            return render(request, 'signup.html', {"error":error, "flag" : 0})
        
        fs = FileSystemStorage()
        if user_image_:               
            fs.save("user_image/" + user_image_.name, user_image_)
            user_image_name = "media/user_image/" + user_image_.name
        else:
            user_image_name = None

        randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        uniqueID = "DreamTrips_" + randomstr


        Useradddata = SignupModel(
            user_id = uniqueID,
            user_firstname = user_firstname_,
            user_lastname = user_lastname_,
            user_username = user_username_,
            user_email = user_email_,
            user_password = make_password(user_password_,salt=randomstr, hasher='argon2'),
            user_image = user_image_name,
            
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

    # except Exception as e:
    #     print("Error", e)
    #     return render(request, 'error404.html')

def loginFun(request):
        messages = ''
        if "userinfo" in request.session:
            if request.session["userinfo"] != None:
                userDetails = request.session["userinfo"]
                return render(request, "index.html",{"userDetails":userDetails, "flag" : 1})
            elif request.session["userinfo"] == None:
                messages = ''
                if request.method == 'POST':
                    userEmail = request.POST['userEmail']
                    password = request.POST['password']
                    if SignupModel.objects.using("default").filter(user_email=userEmail).exists():
                        userdetails = SignupModel.objects.using("default").get(user_email=userEmail)
                    
                        check_pwd = check_password(password, userdetails.user_password)  # Assign check_pwd here
                        if check_pwd:  # Now check_pwd is assigned before using it                            
                            request.session["userinfo"] = {"user_email": userEmail, "user_id": userdetails.user_id , "user_firstname":userdetails.user_firstname , "user_lastname":userdetails.user_lastname,"user_username":userdetails.user_username , "user_password": password,"user_image":userdetails.user_image,"user_city":userdetails.user_city,"user_country":userdetails.user_country,"user_dateofbirth":userdetails.user_dateofbirth,"user_gender":userdetails.user_gender,"user_mobile":userdetails.user_mobile,"user_state":userdetails.user_state}

                            userDetails = request.session["userinfo"]
                            request.session["loginotp"]=None
                            return render(request, "index.html",{"userDetails":userDetails, "flag" : 1})
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
        user_email_ = request.POST.get('useremail')
        if SignupModel.objects.filter(user_email=user_email_).exists():
            
            randomstr = ''.join(random.choices(string.digits, k=6))  
            request.session['otp'] = randomstr
            request.session['user_email'] = user_email_
            
            email_status = mailSend(request, user_email_, randomstr)

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
            
            # Check if user-entered OTP matches the OTP stored in the session
            if user_otp == otp:
                return render(request, 'new_password.html', { "flag" : 1})
                
            else:
                error = "Invalid OTP. Please try again."
                return render(request, 'otp.html', {"error": error, "flag": 0})
        if request.session['loginotp'] is not None:
            loginotp = request.session['loginotp']
            
            # Check if user-entered OTP matches the login OTP stored in the session
            if user_otp == loginotp:
                return render(request, 'login.html', { "flag": 1})
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
            if SignupModel.objects.filter(user_email=user_email).exists():
                user = SignupModel.objects.get(user_email=user_email)
                user.user_password =  make_password(user_new_password,salt=randomstr, hasher='argon2')
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
  
def mybookingFun(request):
    context = {
            "header" : "header header-light",
            "mainheaderClass" : "",
            "headerClass" : "",
            "listheader" : "list-buttons",
            "alistheader" : "bg-primary",

        }
    try:
        userDetails = request.session.get("userinfo")
        
        if userDetails:
            return render(request, 'my_booking.html', {"userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'my_booking.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')

def mywishlistsFun(request):
    context = {
        "header": "header header-theme",
        "mainheaderClass": "",
        "headerClass": "",
        "listheader": "list-buttons light",
        "alistheader": "bg-primary",
    }
    try:
        userDetails = request.session.get("userinfo")

        user_id = userDetails['user_id']
        # selected_flight_id = request.session.get('selected_flight_id')
        # selected_hotel_id = request.session.get('selected_hotel_id')
        # selected_destination_id = request.session.get('selected_destination_id')

        # destination = DestinationModel.objects.get(Destination_id=selected_destination_id)
        # destination_stay = DestinationstayModel.objects.filter(Destination=destination)

        # flight = flightClassModel.objects.get(flightClass_id=selected_flight_id)
        # hotel = destinationHotelModel.objects.get(destinationHotel_id=selected_hotel_id)

        # userwishlist = BillingModel.objects.filter(Billing_user = user_id)
        # print(userwishlist , "LLLLLLLLLLLLLLL")

        if userDetails:
            return render(request, 'my_wishlists.html', {"userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'my_wishlists.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')

def myprofileFun(request):
    context = {
            "header" : "header header-dark",
            "mainheaderClass" : "nav-brand static-show",
            "headerClass" : "mob-show",
            "listheader" : "list-buttons light",
            "alistheader" : "",
        }
    try:
        userDetails = request.session.get("userinfo")
            
        if userDetails:
            if request.method == 'POST':
                user_id = request.POST['user_id']
                user_firstname_ = request.POST['userFirstName']
                user_lastname_ = request.POST['userLastName']
                user_username_ = request.POST['userName']
                user_email_ = request.POST['userEmail']
                user_password_ = request.POST['userPassword']
                user_mobile_ = request.POST['userMobile']
                user_dateofbirth_ = request.POST['userDateOfBirth']
                user_gender_ = request.POST['userGender']
                user_city_ = request.POST['userCity']
                user_state_ = request.POST['userState']
                user_country_ = request.POST['userCountry']
                user_image_ = request.FILES.get('userImage', False)
                

                randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                
                userupdatedata = SignupModel.objects.get(pk=user_id)
                userupdatedata.user_firstname = user_firstname_
                userupdatedata.user_lastname = user_lastname_
                userupdatedata.user_username = user_username_
                userupdatedata.user_email = user_email_
                userupdatedata.user_password = make_password(user_password_,salt=randomstr, hasher='argon2')
                userupdatedata.user_mobile = user_mobile_
                userupdatedata.user_dateofbirth = user_dateofbirth_
                userupdatedata.user_gender = user_gender_
                userupdatedata.user_city = user_city_
                userupdatedata.user_state = user_state_
                userupdatedata.user_country = user_country_


                if user_image_:
                    fs = FileSystemStorage()
                    fs.save("user_image/" + user_image_.name, user_image_)
                    updateuserimage = "media/user_image/" + user_image_.name
                    userupdatedata.user_image = updateuserimage
                else:
                    updateuserimage = userupdatedata.user_image

                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")
                output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")
                userupdatedata.user_created_at_update = output_string


                
                
                request.session["userinfo"] = {"user_email": user_email_, "user_id":  user_id , "user_firstname": user_firstname_ , "user_lastname": user_lastname_,"user_username": user_username_ , "user_password": user_password_,"user_image": updateuserimage,"user_city": user_city_,"user_country": user_country_,"user_dateofbirth": user_dateofbirth_,"user_gender": user_gender_,"user_mobile": user_mobile_,"user_state": user_state_}
                
                userupdatedata.save()
                if userupdatedata.user_id:
                    userDetails = request.session["userinfo"]

                    return render(request, 'my_profile.html',{"context":context, "userDetails":userDetails , "flag" : 1})
                else:
                    error = "Something goes wrong in updation!!"
                    return render(request, 'my_profile.html',{"error":error, "flag" : 0})
            
            return render(request, 'my_profile.html',{"context":context, "userDetails":userDetails , "flag" : 1})

        else:
            return render(request, 'my_profile.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')

def myprofilepasswordFun(request):
    context = {
            "header" : "header header-dark",
            "mainheaderClass" : "nav-brand static-show",
            "headerClass" : "mob-show",
            "listheader" : "list-buttons light",
            "alistheader" : "",
        }
    try:
        userDetails = request.session.get("userinfo")
        if userDetails:
            if request.method == 'POST':
                userDetails = request.session.get("userinfo")
                user_id = request.POST.get('user_id')
                old_password = request.POST.get('oldPassword')
                new_password = request.POST.get('confirmPassword')
                usernewpassworddata = SignupModel.objects.get(pk=user_id)
                # Check if the old password matches
                if not check_password(old_password, usernewpassworddata.user_password):
                    error = 'Old password is incorrect.'
                    return render(request, "my_profile_password.html", {"error": error})
                # Generate random salt and hash the new password
                randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                usernewpassworddata.user_password = make_password(new_password, salt=randomstr, hasher='argon2')
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")
                output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")
                usernewpassworddata.user_created_at_update = output_string
                userDetails['user_password'] = new_password
                request.session["userinfo"] = userDetails
                usernewpassworddata.save()
                if usernewpassworddata.user_id:
                    userDetails = request.session["userinfo"]
                messages.success(request, 'Password updated successfully.')
                return render(request, 'index.html', {"context": context, "userDetails": userDetails, "flag": 1})

            return render(request, 'my_profile_password.html', {"context": context, "userDetails": userDetails, "flag": 1})
        else:
                return render(request, 'login.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')