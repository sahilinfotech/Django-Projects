from django.shortcuts import render, redirect
from adminpanelApp import *
from adminpanelApp.models import *
import json
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  #for File storage
from django.http import HttpResponse, JsonResponse
from datetime import datetime,date
from django.utils import timezone
import random
import string
from PIL import Image
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import barcode
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from io import BytesIO

media_path = "../../../"
# Create your views here.

# def loginFun(request):

#     if "userinfo" in request.session:
#         if request.session["userinfo"] != None:
#             print(request.session["userinfo"],'sssssssssssssssssssssssssssssssss')
#             userDetails = request.session["userinfo"]
#             return render(request, 'index_Add.html', {"userDetails": userDetails})
#         elif request.session["userinfo"] == None:
#             msg = ''
#             if request.method == 'POST':
#                 username = request.POST['username']
#                 password = request.POST['password']
#                 if userModel.objects.using("default").filter(user_username=username).exists():
#                     userdetails = userModel.objects.using("default").get(user_username=username)
#                     if userdetails.user_password != password:
#                         msg = 'Password is Invalid'
#                         return render(request, "signin.html", {"message": msg})
#                     if userdetails.user_password == password and userdetails.user_is_active == "On" :
#                         usertype = userdetails.user_emp_type
#                         useremail = userdetails.user_email

#                         status='0'
#                         if usertype == "admin" or usertype == "manager":
#                             status = "1"
#                         elif usertype == "customer":
#                             status = "2"
#                         elif usertype == "contract" or usertype == "regular":
#                             status = "3"

#                         request.session["userinfo"] = {"usertype" : usertype, "username_loggged": username, "user_id": userdetails.user_id,"useremail": useremail,  "status" : status }
#                         return redirect(dashboardFun)

#                     else:
#                         msg = 'Your account is deactivated please contact to admin'
#                         return render(request, "signin.html", {"message": msg})
#                 else:
#                     msg = 'Username is invalid'
#                     return render(request, "signin.html", {"message": msg})
#             return render(request, "signin.html", {"message": msg})
#     else:
#         msg=''
#         request.session["userinfo"] = None
#         return render(request, "signin.html", {"message": msg})

# def logoutFun(request):
#     try:
#         userDetails = request.session["userinfo"]
#         request.session["userinfo"] = None
#         return redirect(loginFun)
#     except:
#         return render(request, '404_Page.html')

# def forgot_password(request):
#     try:
#         if request.method == 'POST':
#             data_dict = request.POST.get('jsonData')
#             data = json.loads(data_dict)
#             randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))  # Assuming randomstr is a string
#             request.session['randomstr'] = randomstr
#             useremail = data.get('useremail')
#             if userModel.objects.filter(user_email=useremail).exists():
#                 # Generate a password reset link and send it to the user's email
#                 email_status = mailSend(request, useremail, randomstr)
#                 if email_status:
#                     return JsonResponse({'success': True})
#                 else:
#                     return JsonResponse({'error': False, 'message': 'Failed to send email.'})
#             else:
#                 return JsonResponse({'error': False, 'message': 'Email address not found.'})
#         else:
#             # Handle GET request if needed
#             pass
#     except:
#         return render(request, '404_Page.html')

# def otp(request):
#     try:
#         if request.method == 'POST':
#             data_dict = request.POST.get('jsonData')
#             data = json.loads(data_dict)
#             otpcheck = request.session.get('randomstr')
#             userotp = data.get("userotp")
#             if userotp == otpcheck:
#                 return JsonResponse({'success': True})
#             else:
#                 return JsonResponse({'error': False, 'message': 'Please validate otp.'})
#     except:
#         return render(request, '404_Page.html')

# def newpassword(request):
#     try:
#         if request.method == 'POST':
#             data_dict = request.POST.get('jsonData')
#             data = json.loads(data_dict)
#             useremail = data.get("useremail")
#             usernewpassword = data.get("usernewpassword")

#             newpassword_data = userModel.objects.get(user_email=useremail)
#             newpassword_data.user_password = usernewpassword
            
#             now = datetime.now()
#             dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#             input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

#             # Format the datetime object into the desired output format
#             output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

#             newpassword_data.user_created_at_update = output_string


#             newpassword_data.save()

#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'message': 'Please validate otp.'})
#     except:
#         return render(request, '404_Page.html')


def dashboardFun(request):
    return render(request, 'index_Add.html')
        
# Medicine 

# add record in the data in medicineModel_tb table
# def medicineRegisterFun(request):
#     try:

#         if request.method == "POST":

#             medicine_name_ = request.POST['medicineName']
#             medicine_price_ = request.POST['medicinePrice']
#             medicine_quantity_ = request.POST['medicineQuantity']
#             medicine_mg_ = request.POST['medicinemg']
#             medicine_expiry_date_ = request.POST['medicineexpiryDate']
#             medicine_mfg_date_ = request.POST['medicineMfgDate']
#             medicine_is_active_ = request.POST.get('medicinedisable')
            
#             if len(medicine_name_) <= 0:
#                 messages.error(request,'Please Enter Medicine Name!!')
#                 return redirect(medicineRegisterFun)
            
#             if len(medicine_price_) <= 0:
#                 messages.error(request,'Please Enter Medicine Price!!')
#                 return redirect(medicineRegisterFun)
            
#             if len(medicine_quantity_) <= 0:
#                 messages.error(request,'Please Enter Medicine Quantity!!')
#                 return redirect(medicineRegisterFun)
            
#             if len(medicine_mfg_date_) <= 0:
#                 messages.error(request,'Please Enter Medicine MFG Date!!')
#                 return redirect(medicineRegisterFun)
            
#             if len(medicine_expiry_date_) <= 0:
#                 messages.error(request,'Please Enter Medicine expiry Date!!')
#                 return redirect(medicineRegisterFun)
            
#             try:
#                 medicine_expiry_date = datetime.strptime(medicine_expiry_date_, '%Y-%m-%d')
#                 medicine_mfg_date = datetime.strptime(medicine_mfg_date_, '%Y-%m-%d')
#             except ValueError:
#                 messages.error(request, 'Invalid date format!')
#                 return redirect(medicineRegisterFun)
            
#             # Check if expiry date is after manufacturing date
#             if medicine_expiry_date <= medicine_mfg_date:
#                 messages.error(request, 'Expiry date must be after manufacturing date!')
#                 return redirect(medicineRegisterFun)
            
#             # Check if medication is expiryd
#             # if medicine_expiry_date.date() <= timezone.now().date():
#             #     messages.error(request, 'Medication has already expiryd!')
#             #     return redirect(medicineRegisterFun)
            
#             if medicine_is_active_ == "on":
#                 active = True
#             else:
#                 active = False
            
#             randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
#             uniqueID = "medicine_" + randomstr


#             medicine = medicineModel(
#                 medicine_id = uniqueID,
#                 medicine_name = medicine_name_,
#                 medicine_price = medicine_price_,
#                 medicine_quantity = medicine_quantity_,
#                 medicine_remember_quantity = medicine_quantity_,
#                 medicine_mg =medicine_mg_,
#                 medicine_expiry_date = medicine_expiry_date_,
#                 medicine_mfg_date = medicine_mfg_date_,
#                 medicine_is_active = active
#             )

#             medicine.save()

#             if medicine.medicine_id:
#                 messages.success(request, "medicine Data is add succesfully!!")
#                 return render(request, 'medicine_Add.html')
#             else:   
#                 messages.error(request, "Something is wrong!!")
#                 return redirect(medicineRegisterFun)

#         return render(request, 'medicine_Add.html')
#     except:
#         return render(request, 'error404.html')

def medicineRegisterFun(request):
    try:
        if request.method == "POST":
            medicine_name_ = request.POST['medicineName']
            medicine_price_ = request.POST['medicinePrice']
            medicine_quantity_ = request.POST['medicineQuantity']
            medicine_mg_ = request.POST['medicinemg']
            medicine_expiry_date_ = request.POST['medicineexpiryDate']
            medicine_mfg_date_ = request.POST['medicineMfgDate']
            medicine_is_active_ = request.POST.get('medicinedisable')

            if len(medicine_name_) <= 0:
                messages.error(request, 'Please Enter Medicine Name!!')
                return redirect(medicineRegisterFun)

            if len(medicine_price_) <= 0:
                messages.error(request, 'Please Enter Medicine Price!!')
                return redirect(medicineRegisterFun)

            if len(medicine_quantity_) <= 0:
                messages.error(request, 'Please Enter Medicine Quantity!!')
                return redirect(medicineRegisterFun)

            if len(medicine_mfg_date_) <= 0:
                messages.error(request, 'Please Enter Medicine MFG Date!!')
                return redirect(medicineRegisterFun)

            if len(medicine_expiry_date_) <= 0:
                messages.error(request, 'Please Enter Medicine expiry Date!!')
                return redirect(medicineRegisterFun)

            try:
                medicine_expiry_date = datetime.strptime(medicine_expiry_date_, '%Y-%m-%d')
                medicine_mfg_date = datetime.strptime(medicine_mfg_date_, '%Y-%m-%d')
            except ValueError:
                messages.error(request, 'Invalid date format!')
                return redirect(medicineRegisterFun)

            if medicine_expiry_date <= medicine_mfg_date:
                messages.error(request, 'Expiry date must be after manufacturing date!')
                return redirect(medicineRegisterFun)

            if medicine_is_active_ == "on":
                active = True
            else:
                active = False

            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            randomstr_barcode = ''.join(random.choices(string.digits, k=12))

            uniqueID = "medicine_" + randomstr

            # Generate barcode
            barcode_data = randomstr_barcode
            barcodeimagename = medicine_name_ + "_" + medicine_mg_
            barcode_class = barcode.get_barcode_class('code128')
            barcode_instance = barcode_class(barcode_data, writer=ImageWriter())
            barcode_io = BytesIO()
            barcode_instance.write(barcode_io)
            barcode_image_name = f"{barcodeimagename}.png"
            barcode_image_content = ContentFile(barcode_io.getvalue(), name=barcode_image_name)

            medicine = medicineModel(
                medicine_id=uniqueID,
                medicine_name=medicine_name_,
                medicine_price=medicine_price_,
                medicine_quantity=medicine_quantity_,
                medicine_remember_quantity=medicine_quantity_,
                medicine_mg=medicine_mg_,
                medicine_expiry_date=medicine_expiry_date_,
                medicine_mfg_date=medicine_mfg_date_,
                medicine_is_active=active,
                medicine_barcode=barcode_image_content
            )

            medicine.save()

            if medicine.medicine_id:
                messages.success(request, "Medicine Data is added successfully!!")
                return render(request, 'medicine_Add.html')
            else:
                messages.error(request, "Something went wrong!!")
                return redirect(medicineRegisterFun)

        return render(request, 'medicine_Add.html')
    except:
        return render(request, 'error404.html')
    
# View record in the data in medicineModel_tb table 
def medicineViewFun(request):
    try:
        medicine_view = medicineModel.objects.all()
        
        return render(request, 'medicine_View_Table.html',{"medicine_view": medicine_view})
    except:
            return render(request, 'error404.html')
    
# Featch the data for particular id and dispaly all data in html page
def medicineViewdetailsFun(request,medicine_id):
    try:
        medicine_details = medicineModel.objects.get(pk=medicine_id)
        return render(request, 'medicine_View_Details.html',{'medicine_details':medicine_details})
    except:
        return render(request, 'error404.html')
    
# Featch the data for particular id and dispaly all data in html page
def medicineFetchFun(request,medicine_id):
    try:
        medicine_featch = medicineModel.objects.get(pk=medicine_id)
        return render(request, 'medicine_Edit.html',{"medicine_featch": medicine_featch})
    except:
        return render(request, 'error404.html')

# Edit the data for particular id and dispaly all data in html page
def medicineEditFun(request):
    try:

        if request.method == 'POST':
        # Get data from the form
            medicine_id = request.POST['medicine_id']
            medicine_name_ = request.POST['medicineName']
            medicine_price_ = request.POST['medicinePrice']
            medicine_quantity_ = request.POST['medicineQuantity']
            medicine_remember_quantity_ = request.POST['medicineRememberQuantity']
            medicine_mg_ = request.POST['medicinemg']
            medicine_expiry_date_ = request.POST['medicineexpiryDate']
            medicine_mfg_date_ = request.POST['medicineMfgDate']
            medicine_is_active_ = request.POST.get('medicinedisable')

            if len(medicine_name_) <= 0:
                messages.error(request,'Please Enter medicine Name!!')
                return redirect(medicineFetchFun,medicine_id)
        
            if len(medicine_price_) <= 0:
                messages.error(request,'Please Enter medicine Price!!')
                return redirect(medicineFetchFun,medicine_id)
            
            if len(medicine_quantity_) <= 0:
                messages.error(request,'Please Enter medicine Quantity!!')
                return redirect(medicineFetchFun,medicine_id)
            
            if len(medicine_mfg_date_) <= 0:
                messages.error(request,'Please Enter Medicine MFG Date!!')
                return redirect(medicineFetchFun,medicine_id)
        
            if len(medicine_expiry_date_) <= 0:
                messages.error(request,'Please Enter Medicine expiry Date!!')
                return redirect(medicineFetchFun,medicine_id)
            
            if medicine_is_active_ == "on":
                active = True
            else:
                active = False
            
            medicine_data = medicineModel.objects.get(pk=medicine_id)
            medicine_data.medicine_name = medicine_name_
            medicine_data.medicine_price = medicine_price_
            medicine_data.medicine_quantity = medicine_quantity_
            medicine_data.medicine_remember_quantity = medicine_remember_quantity_
            medicine_data.medicine_mg = medicine_mg_
            medicine_data.medicine_mfg_date = medicine_mfg_date_
            medicine_data.medicine_expiry_date = medicine_expiry_date_
            medicine_data.medicine_is_active = active

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

            # Format the datetime object into the desired output format
            output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

            medicine_data.medicine_created_at_update = output_string


            medicine_data.save()
            if medicine_data.medicine_id:
                messages.success(request, "medicine Data Update !!")
                return redirect(medicineViewFun)
            else:
                messages.error(request, "Something goes wrong in updation!!")
                return redirect(medicineFetchFun,medicine_id)

        return render(request, 'medicine_Edit.html')
    except:
        return render(request, 'error404.html')
    
# delete record in the data in medicineModel_tb table
def medicineDeleteFun(request,medicine_id):
    try:
        if medicineModel.objects.filter(pk=medicine_id).exists():
            datadel = medicineModel.objects.get(pk=medicine_id)
            datadel.delete()
            messages.success(request, "medicine Data Delete succesfully!!")
        return redirect(medicineViewFun)
    except:
        return render(request, 'error404.html')



def outofstockViewFun(request):
    outofstock_view = medicineModel.objects.filter(medicine_remember_quantity = 0)
    print(outofstock_view ,"grishaaaaaaaa")
    return render(request, 'outofstock.html',{"outofstock_view": outofstock_view })



def expirymedicineViewFun(request):
    today = date.today()
    expirymedicine_view = medicineModel.objects.filter(medicine_expiry_date__lte=today)
    print(expirymedicine_view)  # Print the queryset to check if it contains any medicines
    return render(request, 'expirymedicine_View_Table.html', {"expirymedicine_view": expirymedicine_view})



'''
        Sell Medicine (insert)
        Request : POST
        Data :{
                    "sellmedicine_id": "Medicine_sellmedicine_wq5d3s8ubye17zf",
                    "analysis" : "Text Analysis",
                    "sellmedicine_is_active" = "True/False"
                }
    '''
# add record in the data in sellmedicineModel_tb table
def sellmedicineRegisterFun(request):
    # try:
    medicine_view = medicineModel.objects.all()
    
    if request.method == "POST":
        medicine_ = request.POST['medicineModel']
        # sellmedicine_price_ = request.POST['sellmedicinePrice']
        sellmedicine_quantity_ = request.POST['sellmedicineQuantity']
        sellmedicine_remember_quantity_ = request.POST['sellmedicineRememberQuantity']
        sellmedicine_is_active_ = request.POST.get('sellmedicinedisable')
        
        if medicine_ == "select":
            messages.error(request, "Please select Medicine Name !!")
            return redirect(sellmedicineRegisterFun)
        
        if len(sellmedicine_quantity_) <= 0:
            messages.error(request,'Please Enter Medicine Quantity!!')
            return redirect(sellmedicineRegisterFun)
        
        if sellmedicine_is_active_ == "on":
            active = True
        else:
            active = False
        
        fs = FileSystemStorage()
        
        randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        uniqueID = "sellmedicine_" + randomstr

        medicineinstance = medicineModel.objects.get(pk=medicine_)


        sellmedicine = sellmedicineModel(
            sellmedicine_id = uniqueID,
            medicine = medicineinstance,
            sellmedicine_name = medicineinstance.medicine_name,
            sellmedicine_quantity = sellmedicine_quantity_,
            sellmedicine_remember_quantity = sellmedicine_remember_quantity_,
            sellmedicine_is_active = active
        )

        sellmedicine.save()

        if sellmedicine.sellmedicine_id:
            messages.success(request, "Sell Medicine Data is add succesfully!!")
            return render(request, 'sellmedicine_Add.html',{"medicine_view":medicine_view})
        else:   
            messages.error(request, "Something is wrong!!")
            return redirect(sellmedicineRegisterFun) 
    
    return render(request, 'sellmedicine_Add.html',{"medicine_view":medicine_view})
    # except:
    #     return render(request, 'error404.html')
    
# View record in the data in sellmedicineModel_tb table 
def sellmedicineViewFun(request):
    # try:
    
    sellmedicine_view = sellmedicineModel.objects.all() 
    return render(request, 'sellmedicine_View_Table.html',{"sellmedicine_view": sellmedicine_view })
    # except:
    #     return render(request, 'error404.html')
    
# Featch the data for particular id and dispaly all data in html page
def sellmedicineViewdetailsFun(request,sellmedicine_id):
    try:
    
        sellmedicine_details = sellmedicineModel.objects.get(pk=sellmedicine_id)
        
        return render(request, 'sellmedicine_View_Details.html',{'sellmedicine_details':sellmedicine_details})
    except:
        return render(request, 'error404.html')
    
# # Featch the data for particular id and dispaly all data in html page
def sellmedicineFetchFun(request,sellmedicine_id):
    # try:
    sellmedicine_featch = sellmedicineModel.objects.get(pk=sellmedicine_id)
    return render(request, 'sellmedicine_Edit.html',{"sellmedicine_featch": sellmedicine_featch })
    # except:
    #     return render(request, 'error404.html')
    
'''
        Sell Medicine  (Edit)
        Request : POST
        Data :{
                    "sellmedicine_id": "Medicine_sellmedicine_wq5d3s8ubye17zf",
                    "analysis" : "text Analysis",
                    "sellmedicine_is_active" = "True/False"
                }
    '''
# Edit the data for particular id and dispaly all data in html page
def sellmedicineEditFun(request):
    try:
    
        if request.method == 'POST':
        # Get data from the form
            sellmedicine_id = request.POST['sellmedicine_id']
            dashboard_ = request.POST['dashboardname']
            analysis_ = request.POST['analysistype']
            sellmedicine_is_active_ = request.POST.get('sellmedicinedisable')

            if dashboard_ == "select":
                messages.error(request, "Please select Medicine Name !!")
                return redirect(sellmedicineFetchFun,sellmedicine_id)
            
            if sellmedicine_is_active_ == "on":
                active = True
            else:
                active = False
            
            dashboardinstance = medicineModel.objects.get(categoryDashboard_title=dashboard_)
            analysisinstance = medicineModel.objects.get(analysisType_type=analysis_)


            sellmedicine_data = sellmedicineModel.objects.get(pk=sellmedicine_id)
            sellmedicine_data.dashboard = dashboardinstance
            sellmedicine_data.analysis = analysisinstance
            sellmedicine_data.sellmedicine_is_active = active

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

            # Format the datetime object into the desired output format
            output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

            sellmedicine_data.sellmedicine_created_at_update = output_string


            sellmedicine_data.save()
            if sellmedicine_data.sellmedicine_id:
                messages.success(request, "Sell Medicine Data Update !!")
                return redirect(sellmedicineViewFun)
            else:
                messages.error(request, "Something goes wrong in updation!!")
                return redirect(sellmedicineFetchFun,sellmedicine_id)
        
        return render(request, 'sellmedicine_Edit.html')
    except:
        return render(request, 'error404.html')
    
# delete record in the data in sellmedicineModel_tb table
def sellmedicineDeleteFun(request,sellmedicine_id):
    try:
        if sellmedicineModel.objects.filter(pk=sellmedicine_id).exists():
            datadel = sellmedicineModel.objects.get(pk=sellmedicine_id)
            datadel.delete()
            messages.success(request, "Sell Medicine Data Delete succesfully!!")
        return redirect(sellmedicineViewFun)
    except:
        return render(request, 'error404.html')



def medicinedatafetchFun(request, medicine_name):
    try:
        medicines = medicineModel.objects.filter(medicine_name=medicine_name)
        
        if medicines.exists():
            selected_medicine = medicines.latest('medicine_created_at')
            
            # Fetching available mg values for the selected medicine
            available_mgs = medicineModel.objects.filter(medicine_name=medicine_name).values_list('medicine_mg', flat=True).distinct()
    
            # Fetching prices and quantities for each mg
            prices = []
            quantities = []
            medicine_id = []
            for mg in available_mgs:
                medicine = medicineModel.objects.filter(medicine_name=medicine_name, medicine_mg=mg).latest('medicine_created_at')
                medicine_id.append(medicine.medicine_id)
                prices.append(medicine.medicine_price)
                quantities.append(medicine.medicine_remember_quantity)
                
                data = {
                    'medicine_id': medicine_id,
                    'medicine_name': selected_medicine.medicine_name,
                    'medicine_price': prices,
                    'medicine_quantity': quantities,
                    'medicineMgs': list(available_mgs),
                }
            print(data) 
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Medicine not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def patientdetailRegisterFun(request):
    try:
        if request.method == 'POST':

            patientdetail_name_ = request.POST.get('patientdetailName')
            patientdetail_doctor_name_ = request.POST.get('patientdetailDoctorName')
            patientdetail_diseases_description_ = request.POST.get('patientdetailDiseasesDescription')
            patientdetail_mobile_no_ = request.POST.get('patientdetailMobileNo')
            
            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            uniqueID = "patient_detail_" + randomstr

            patient_detail = {
                'patientdetail_id': uniqueID,
                'patientdetail_name': patientdetail_name_,
                'patientdetail_doctor_name': patientdetail_doctor_name_,
                'patientdetail_diseases_description': patientdetail_diseases_description_,
                'patientdetail_mobile_no': patientdetail_mobile_no_
            }


            request.session['patient_detail'] = patient_detail
            return redirect(patientmedicineRegisterFun)
        
        return render(request, 'patient_detail_Add.html')
    except:
        return render(request, 'error404.html')

# View record in the data in patientdetailModel_tb table 
def patientdetailViewFun(request):
    try:

        patientdetail_view = patientdetailModel.objects.all() 
        return render(request, 'patient_detail_View_Table.html',{"patientdetail_view": patientdetail_view })
    
    except:
        return render(request, 'error404.html')
    
# Featch the data for particular id and dispaly all data in html page
def patientdetailViewdetailsFun(request,patientdetail_id):
    try:
    
        patient_detail = patientdetailModel.objects.get(pk=patientdetail_id)
        patient_medicine_details = patientmedicineModel.objects.filter(patientdetail=patient_detail)
        
        return render(request, 'patient_detail_View_Details.html',{"patient_medicine_details":patient_medicine_details,'patient_detail':patient_detail})
    except:
        return render(request, 'error404.html')
    
def patientdetailEditFun(request):
    patient_detail = request.session.get('patient_detail')
    try:
        if request.method == 'POST':

            patientdetail_name_ = request.POST.get('patientdetailName')
            patientdetail_doctor_name_ = request.POST.get('patientdetailDoctorName')
            patientdetail_diseases_description_ = request.POST.get('patientdetailDiseasesDescription')
            patientdetail_mobile_no_ = request.POST.get('patientdetailMobileNo')
            
            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            uniqueID = "patient_detail_" + randomstr

            patient_detail = {
                'patientdetail_id': uniqueID,
                'patientdetail_name': patientdetail_name_,
                'patientdetail_doctor_name': patientdetail_doctor_name_,
                'patientdetail_diseases_description': patientdetail_diseases_description_,
                'patientdetail_mobile_no': patientdetail_mobile_no_
            }


            request.session['patient_detail'] = patient_detail
            return redirect(patientmedicineRegisterFun)
        
        return render(request, 'patient_detail_Edit.html',{"patient_detail":patient_detail})
    except:
        return render(request, 'error404.html')

# delete record in the data in patientdetailModel_tb table
def patientdetailDeleteFun(request,patientdetail_id):
    try:
        if patientdetailModel.objects.filter(pk=patientdetail_id).exists():
            datadel = patientdetailModel.objects.get(pk=patientdetail_id)
            datadel.delete()
            messages.success(request, "Patient Bill Data Delete succesfully!!")
        return redirect(patientdetailViewFun)
    except:
        return render(request, 'error404.html')


def patientmedicineRegisterFun(request):
    try:
        # medicine_view = medicineModel.objects.all().values()
        medicine_view = medicineModel.objects.values('medicine_name').distinct()

        if request.method == 'POST':
            medicine_ = request.POST.get('medicineModel')
            medicine_remember_quantity_ = request.POST.get('medicineQuantity')
            patientmedicine_medicine_name_ = request.POST.get('patientMedicineName')
            patientmedicine_price_ = request.POST.get('patientMedicinePrice')
            patientmedicine_mg_ = request.POST.get('patientMedicineMg')
            patientmedicine_quantity_ = request.POST.get('patientMedicineQuantity')
            patientmedicine_remember_quantity_ = request.POST.get('patientMedicineRememberQuantity')
            patientmedicine_totalprice_ = request.POST.get('patientMedicineTotalPrice')

            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            uniqueID = "patient_medicine_" + randomstr

            medicine_data = {
                'medicine': medicine_,
                'patientmedicine_id': uniqueID,
                'medicine_remember_quantity_': medicine_remember_quantity_,
                'patientmedicine_medicine_name': patientmedicine_medicine_name_,
                'patientmedicine_price': patientmedicine_price_,
                'patientmedicine_mg': patientmedicine_mg_,
                'patientmedicine_quantity': patientmedicine_quantity_,
                'patientmedicine_remember_quantity': patientmedicine_remember_quantity_,
                'patientmedicine_totalprice': patientmedicine_totalprice_
            }

            patient_medicines = request.session.get('patient_medicines', [])
            patient_medicines.append(medicine_data)
            request.session['patient_medicines'] = patient_medicines

            total_price = sum(float(medicine['patientmedicine_totalprice']) for medicine in patient_medicines)
            patientdetail_totalprice_ = "{:.2f}".format(total_price)
            request.session['patientdetail_totalprice_'] = patientdetail_totalprice_

            return redirect(patientmedicineRegisterFun)

        return render(request, 'patient_medicine_Add.html', {"medicine_view": medicine_view})
    except:
        return render(request, 'error404.html')


def patientmedicineEditFun(request, patientmedicine_id):
    try:
        medicine_view = medicineModel.objects.values('medicine_name').distinct()

        # Fetch the medicine details from the session
        patient_medicines = request.session.get('patient_medicines', [])
        medicine_to_edit = next((medicine for medicine in patient_medicines if medicine['patientmedicine_id'] == patientmedicine_id), None)

        if not medicine_to_edit:
            messages.error(request, "Medicine not found in session.")
            return redirect(patient_bill)  # Adjust this redirect to your correct view name

        if request.method == 'POST':
            # Update medicine details
            medicine_to_edit['medicine'] = request.POST.get('medicineModel')
            medicine_to_edit['patientmedicine_medicine_name'] = request.POST.get('patientMedicineName')
            medicine_to_edit['patientmedicine_price'] = request.POST.get('patientMedicinePrice')
            medicine_to_edit['patientmedicine_mg'] = request.POST.get('patientMedicineMg')
            medicine_to_edit['patientmedicine_quantity'] = request.POST.get('patientMedicineQuantity')
            medicine_to_edit['patientmedicine_remember_quantity'] = request.POST.get('patientMedicineRememberQuantity')
            medicine_to_edit['patientmedicine_totalprice'] = request.POST.get('patientMedicineTotalPrice')

            # Update the session with the edited medicine details
            updated_medicines = [medicine if medicine['patientmedicine_id'] != patientmedicine_id else medicine_to_edit for medicine in patient_medicines]
            request.session['patient_medicines'] = updated_medicines

            # Recalculate the total price and update the session
            total_price = sum(float(medicine['patientmedicine_totalprice']) for medicine in updated_medicines)
            patientdetail_totalprice_ = "{:.2f}".format(total_price)
            request.session['patientdetail_totalprice_'] = patientdetail_totalprice_

            # messages.success(request, "Patient Medicine Data Updated Successfully!!")
            return redirect(patient_bill)  # Adjust this redirect to your correct view name

        return render(request, 'patient_medicine_Edit.html', {"medicine_view": medicine_view, "medicine_to_edit": medicine_to_edit})
    except Exception as e:
        messages.error(request, "An error occurred: " + str(e))
        return render(request, 'error404.html')


# delete record in the data in patientdetailModel_tb table
def patientmedicineDeleteFun(request, patientmedicine_id):
    try:
        patient_medicines = request.session.get('patient_medicines', [])
        updated_medicines = [medicine for medicine in patient_medicines if str(medicine['patientmedicine_id']) != str(patientmedicine_id)]
        request.session['patient_medicines'] = updated_medicines

        total_price = sum(float(medicine['patientmedicine_totalprice']) for medicine in updated_medicines)
        patientdetail_totalprice_ = "{:.2f}".format(total_price)
        request.session['patientdetail_totalprice_'] = patientdetail_totalprice_

        if patientmedicineModel.objects.filter(pk=patientmedicine_id).exists():
            datadel = patientmedicineModel.objects.get(pk=patientmedicine_id)
            datadel.delete()
        
        messages.success(request, "Patient Medicine Data Deleted Successfully!!")
        return redirect(patient_bill)  # Adjust this redirect to your correct view name

    except Exception as e:
        messages.error(request, "An error occurred: " + str(e))
        return render(request, 'error404.html')

    
def patient_bill(request):
    patient_detail = request.session.get('patient_detail')
    patientdetail_totalprice_ = request.session.get('patientdetail_totalprice_')
    patient_medicines = request.session.get('patient_medicines', [])
    print(patient_medicines , "Nowwwww")

    try:
        if request.method == 'POST':

            patient_detail_object = patientdetailModel(
                patientdetail_id=patient_detail['patientdetail_id'],
                patientdetail_name=patient_detail['patientdetail_name'],
                patientdetail_doctor_name=patient_detail['patientdetail_doctor_name'],
                patientdetail_diseases_description=patient_detail['patientdetail_diseases_description'],
                patientdetail_mobile_no=patient_detail['patientdetail_mobile_no'],
                patientdetail_totalprice=patientdetail_totalprice_
            )
            patient_detail_object.save()

            for medicine_data in patient_medicines:
                patient_medicine_object = patientmedicineModel(
                    patientmedicine_id=medicine_data['patientmedicine_id'],
                    medicine_id=medicine_data['medicine'],
                    patientdetail=patient_detail_object,
                    patientmedicine_medicine_name=medicine_data['patientmedicine_medicine_name'],
                    patientmedicine_price=medicine_data['patientmedicine_price'],
                    patientmedicine_mg=medicine_data['patientmedicine_mg'],
                    patientmedicine_quantity=medicine_data['patientmedicine_quantity'],
                    patientmedicine_remember_quantity=medicine_data['patientmedicine_remember_quantity'],
                    patientmedicine_totalprice=medicine_data['patientmedicine_totalprice']
                )
                patient_medicine_object.save()

            # Retrieve the medicineModel instance
                medicine_instance = medicineModel.objects.get(medicine_id=medicine_data['medicine'])

                # Update and save the medicine_remember_quantity
                medicine_instance.medicine_remember_quantity = medicine_data['patientmedicine_remember_quantity']
                medicine_instance.save()

            # Clear session data
            del request.session['patient_detail']
            del request.session['patient_medicines']
            return redirect(patientdetailViewFun)
        
        return render(request, 'patient_bill.html', {'patient_detail':patient_detail,'patientdetail_totalprice_': patientdetail_totalprice_ , "patient_medicines":patient_medicines})
    except:
        return render(request, 'error404.html')
    
