from django.shortcuts import render, redirect
from ProductAR import *
from ProductAR.models import *
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
from ProductAR.emailsend import *
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
                return redirect(customizeViewFun)
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
                            return redirect(customizeViewFun)
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
        else:
            return redirect(loginFun)
        return render(request, 'Product.html',{"context":context,"userDetails": userDetails, "flag" : 1})
    else:
        return redirect(loginFun)
    
def productDetailsFun(request):
    context = {
    "optionClass" : "others-option",   
    }
    
    if request.session["userinfo"] != None:
        if "userinfo" in request.session:
            userDetails = request.session["userinfo"]
        else:
            return redirect(loginFun)
        return render(request, 'ProductDetails.html',{"context":context,"userDetails": userDetails, "flag" : 1})
    else:
        return redirect(loginFun)
        
def customizeFun(request):

    context = {
    "optionClass" : "others-option",   
    }

    try: 
    
        if request.session["userinfo"] != None:

            if "userinfo" in request.session:

                userDetails = request.session["userinfo"]

                if request.method == "POST":

                    customize_image_ = request.FILES.get('customizeImage', False)

                    if not customize_image_:
                        error = "Please Select Customize Photo !!"
                        return render(request, 'customize.html', {"error":error, "flag" : 0})
                    
                    fs = FileSystemStorage()
                    
                    fs.save("productAR/customize_photo/" + customize_image_.name, customize_image_)

                    randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                    uniqueID = "ProductAR_customize_" + randomstr

                    imgpath = '/media/productAR/customize_photo/' + customize_image_.name
                    data= request.session['userinfo']
                    usermodelinstance = userModel.objects.get(pk = data['user_id'])
                    customizedata = customizeModel(
                        customize_id = uniqueID,
                        user = usermodelinstance,
                        customize_image = imgpath,
                    )

                    customizedata.save()

                    if customizedata.customize_id:
                        request.session["customize_id"] = uniqueID
                        return render(request, 'productar.html',{"userDetails": userDetails,"context":context,"imagepath":imgpath, "flag" : 1})

                    else:   
                        error = "Something is wrong!!"
                        return render(request, 'customize.html',{"error":error,"flag" : 0})
            else:

                return redirect(loginFun)

            return render(request, 'customize.html',{"context":context,"userDetails": userDetails, "flag" : 1})

        else:

            return redirect(loginFun)

    except Exception as e:

        print(e)
        return render(request, '404_Page.html')

def upload_video(request):
    try: 
        if request.session["userinfo"] != None:
            if "userinfo" in request.session:
                userDetails = request.session["userinfo"]
                customize_id = request.session.get("customize_id")

                if request.method == 'POST' and request.FILES.get('video') and customize_id:
                    video_file = request.FILES['video']
                    customize_video_AmbientLight_ = request.POST['AmbientLight']
                    customize_video_PointLight_ = request.POST['PointLight']
                    customize_video_DirectionalLight_ = request.POST['DirectionalLight']
                    customize_video_SpotLight_ = request.POST['SpotLight']
                    customize_video_Dimension_ = request.POST['Dimension']

                    video_name = generate_random_string() + ".webm"
                    video_path = os.path.join("media", "productAR", "shirt_pattern")
                    fullpath = os.path.join(settings.BASE_DIR, video_path, video_name)

                    os.makedirs(os.path.dirname(fullpath), exist_ok=True)

                    with open(fullpath, 'wb+') as destination:
                        for chunk in video_file.chunks():
                            destination.write(chunk)

                    download_link = settings.BASE_URL + "media/productAR/shirt_pattern/" + video_name

                    # Get the customization instance associated with the stored ID
                    customization_instance = customizeModel.objects.get(customize_id=customize_id)

                    # Update the customization instance with the video path and link
                    customization_instance.customize_video_path = fullpath
                    customization_instance.customize_video_download_link = download_link
                    customization_instance.customize_video_AmbientLight = customize_video_AmbientLight_
                    customization_instance.customize_video_PointLight = customize_video_PointLight_
                    customization_instance.customize_video_DirectionalLight = customize_video_DirectionalLight_
                    customization_instance.customize_video_SpotLight = customize_video_SpotLight_
                    customization_instance.customize_video_Dimension = customize_video_Dimension_
                    customization_instance.save()

                    return JsonResponse({'status': 'success', 'download_link': download_link,"userDetails": userDetails,"flag" : 1})
                else:
                    return JsonResponse({'status': 'error'}, status=400)
            else:
                return redirect(loginFun)
        else:

            return redirect(loginFun)

    except Exception as e:

        print(e)
        return render(request, '404_Page.html')
    
def customizeViewFun(request):
    context = {
    "optionClass" : "others-option",   
    }
    try:
        if request.session["userinfo"] != None:
            if "userinfo" in request.session:
                userDetails = request.session["userinfo"]
                user_id = userDetails['user_id']
                customizeviewtable = customizeModel.objects.filter(user_id=user_id)
            else:
                return redirect(loginFun)
            return render(request, 'customize_view_table.html',{"customizeviewtable":customizeviewtable,"context": context , "userDetails": userDetails,"flag" : 1})
        else:
            return redirect(loginFun)
    except Exception as e:

        print(e)
        return render(request, '404_Page.html')
    
def customizeViewDetailsFun(request,customize_id):
    context = {
    "optionClass" : "others-option",   
    }
    try:
        if request.session["userinfo"] != None:
            userDetails = request.session["userinfo"]
            uploadvideo_viewdetails = customizeModel.objects.get(pk=customize_id)  
            customizevideoview =  media_path + uploadvideo_viewdetails.customize_image
            return render(request, 'productar_view_details.html',{"context":context,"uploadvideo_viewdetails": uploadvideo_viewdetails,"customizevideoview":customizevideoview,"userDetails":userDetails,"flag" : 1})
        else:
            return redirect(loginFun)
    
    except Exception as e:

        print(e)
        return render(request, '404_Page.html')
      
def uploadvideoFetchFun(request,customize_id):
    context = {
    "optionClass" : "others-option",   
    }
    try:
        if request.session["userinfo"] != None:
            userDetails = request.session["userinfo"]
            uploadvideo_featch = customizeModel.objects.get(pk=customize_id)  
            customizevideoview =  media_path + uploadvideo_featch.customize_image
            return render(request, 'productar_edit.html',{"context":context,"uploadvideo_featch": uploadvideo_featch,"customizevideoview":customizevideoview,"userDetails":userDetails,"flag" : 1})
        else:
            return redirect(loginFun)
    
    except Exception as e:

        print(e)
        return render(request, '404_Page.html')
    
def uploadvideoEditFun(request):
    context = {
    "optionClass" : "others-option",   
    }
    try: 
        if request.session["userinfo"] != None:
            if "userinfo" in request.session:
                userDetails = request.session["userinfo"]
                user_id = userDetails['user_id']
                if request.method == 'POST':
                    customize_id = request.POST.get('customize_id')
                    # video_file = request.FILES['video']
                    customize_video_AmbientLight_ = request.POST.get('AmbientLight')
                    customize_video_PointLight_ = request.POST.get('PointLight')
                    customize_video_DirectionalLight_ = request.POST.get('DirectionalLight')
                    customize_video_SpotLight_ = request.POST.get('SpotLight')
                    customize_video_Dimension_ = request.POST.get('Dimension')

                    # video_name = generate_random_string() + ".webm"
                    # video_path = os.path.join("media", "productAR", "shirt_pattern")
                    # fullpath = os.path.join(settings.BASE_DIR, video_path, video_name)

                    # os.makedirs(os.path.dirname(fullpath), exist_ok=True)

                    # with open(fullpath, 'wb+') as destination:
                    #     for chunk in video_file.chunks():
                    #         destination.write(chunk)

                    # download_link = settings.BASE_URL + "media/productAR/shirt_pattern/" + video_name
                        
                    customizationdata = customizeModel.objects.get(pk=customize_id)
                    # customizationdata.customize_video_path = video_path
                    # customizationdata.customize_video_download_link = download_link
                    customizationdata.customize_video_AmbientLight = customize_video_AmbientLight_
                    customizationdata.customize_video_PointLight = customize_video_PointLight_
                    customizationdata.customize_video_DirectionalLight = customize_video_DirectionalLight_
                    customizationdata.customize_video_SpotLight = customize_video_SpotLight_
                    customizationdata.customize_video_Dimension = customize_video_Dimension_
                    customizationdata.save()

                    return JsonResponse({'status': 'success', "userDetails": userDetails,"flag" : 1})
                else:
                        return JsonResponse({'status': 'error'}, status=400)

            else:
                return redirect(loginFun)
        else:
            return redirect(loginFun)
    
    except Exception as e:

        print(e)
        return render(request, '404_Page.html')

    

    
def customizeDeleteFun(request, customize_id):
    try:
        if request.session.get("userinfo"):
            if customizeModel.objects.filter(pk=customize_id).exists():
                customizedatadel = customizeModel.objects.get(pk=customize_id)
                image_path = os.path.join(settings.MEDIA_ROOT, str(customizedatadel.customize_image).replace(settings.MEDIA_URL, ''))
                video_path = customizedatadel.customize_video_path
                if os.path.exists(image_path): 
                    os.remove(image_path)

                if os.path.exists(video_path): 
                    os.remove(video_path)  

                customizedatadel.delete()
                messages.error(request,"Customize Data Deleted Successfully!!")
                return redirect(customizeViewFun)
                
            else:
                messages.error(request, "Customize Data not found!")
                return redirect(customizeViewFun)
        else:
            return redirect(loginFun)
    except Exception as e:

        print(e)
        return render(request, '404_Page.html')
    

