from django.shortcuts import render

from django.shortcuts import render, redirect
from adminpanel.models import bangalowModel,visitorModel,clientModel,moneyManagementModel,resumeModel
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  #for File storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils import timezone
import random
import string
import os
# from PIL import Image
import io
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.

media_path = "../../../"
resume_path = "../../"

def demoFun(request):
        return render(request, 'demo.html')
    
def indexRegisterFun(request):
    if "userinfo" in request.session:
        return render(request, 'index_Add.html')
    # else:
    #     return redirect(loginFun)



# Bangalows Details 
'''
        Bangalows Details (insert)
        Request : POST
        Data :{
                    "bangalow_id": "Pacific_Homes_Bangalow_wq5d3s8ubye17zf",
                    "bangalow_no" : "101",
                    "bangalow_bHK": "2 BHk",
                    "bangalow_area": "15000"
                    "bangalow_price" = "65lakh"
                    "bangalow_is_active" = "On/Off"
                }
    '''
# add record in the data in bangalowmodel_tb table
def bangalowRegisterFun(request):
    if request.method == "POST":

        bangalow_no_ = request.POST.get('bangalowNo')
        bangalow_bhk_ = request.POST.get('bangalowBHK')
        bangalow_area_ = request.POST.get('bangalowArea')
        bangalow_price_ = request.POST.get('bangalowPrice')
        bangalow_is_active_ = request.POST.get('bangalowdisable')
        
        if bangalowModel.objects.filter(bangalow_no=bangalow_no_).exists():
            messages.error(request,'Bangalow No is already existed!!')
            return redirect(bangalowRegisterFun)
        
        if bangalow_no_.isalpha():
            messages.error(request, 'Please Enter a Valid Bangalow No. (at least one digit is required)')
            return redirect(bangalowRegisterFun)

        if len(bangalow_bhk_) <= 0:
            messages.error(request,'Please Enter Bangalow BHK!!')
            return redirect(bangalowRegisterFun)
        
        if len(bangalow_area_) <= 0:
            messages.error(request, "Please Enter Bangalow Area !!")
            return redirect(bangalowRegisterFun)
        
        if len(bangalow_price_) <= 0:
            messages.error(request, "Please Enter Bangalow Price !!")
            return redirect(bangalowRegisterFun)
        
        if not bangalow_price_.isdigit():
                messages.error(request, 'Please Enter A Valid Bangalow Price. (only digits are allowed)')
                return redirect(bangalowRegisterFun)

        if bangalow_is_active_ == None:
            active = "Off"
        else:
            active = "On" 


        randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        uniqueID = "Pacific_Homes_Bangalow_" + randomstr


        bangalow = bangalowModel(
            bangalow_id = uniqueID,
            bangalow_no = bangalow_no_,
            bangalow_bHK = bangalow_bhk_,
            bangalow_area = bangalow_area_,
            bangalow_price = bangalow_price_,
            bangalow_is_active = active
        )

        bangalow.save()

        if bangalow.bangalow_id:
            messages.success(request, "Bangalow is add succesfully!!")
            return redirect(bangalowRegisterFun)
        else:
            messages.error(request, "Something is wrong!!")
            return redirect(bangalowRegisterFun)
    
    return render(request, 'Bangalow_Add.html')

# View record in the data in bangalowmodel_tb table 
def bangalowViewFun(request):
    bangalow_view = bangalowModel.objects.all()
    # bangalowview = bangalowModel.objects.get(pk=bangalow_id)

    # bangalow_actives = request.POST.get('bangalowdisable')
    
    # if bangalow_actives != False:
    #     if bangalow_actives == None:
    #         active = "Off"
    #     else:
    #         active = "On"
    # else:
    #     bangalowsactives = bangalow_view.bangalow_is_active 

    # bangalow_view.bangalow_is_active = bangalowsactives
    
    return render(request, 'Bangalow_View_Table.html',{"bangalow_view": bangalow_view})

# Featch the data for particular id and dispaly all data in html page
def bangalowViewdetailsFun(request,bangalow_id):
    bangalow_details = bangalowModel.objects.get(pk=bangalow_id)
    return render(request, 'Bangalow_View_Details.html',{'bangalow_details':bangalow_details})

# Featch the data for particular id and dispaly all data in html page
def bangalowFetchFun(request,bangalow_id):
    bangalow_featch = bangalowModel.objects.get(pk=bangalow_id)
    return render(request, 'Bangalow_Edit.html',{"bangalow_featch": bangalow_featch})

'''
        Bangalows Details (Edit)
        Request : POST
        Data :{
                    "bangalow_id": "Pacific_Homes_Bangalow_wq5d3s8ubye17zf",
                    "bangalow_no" : "101",
                    "bangalow_bHK": "2 BHk",
                    "bangalow_area": "15000"
                    "bangalow_price" = "65lakh"
                    "bangalow_is_active" = "On/Off"
                }
    '''
# Edit the data for particular id and dispaly all data in html page
def bangalowEditFun(request):
    if request.method == 'POST':
    # Get data from the form
        bangalow_id = request.POST.get('bangalow_id')
        bangalow_no_ = request.POST.get('bangalowNo')
        bangalow_bhk_ = request.POST.get('bangalowBHK')
        bangalow_area_ = request.POST.get('bangalowArea')
        bangalow_price_ = request.POST.get('bangalowPrice')
        bangalow_is_active_ = request.POST.get('bangalowdisable')

        if len(bangalow_no_) <= 0:
            messages.error(request,'Bangalow No is required!!')
            return redirect(bangalowFetchFun,bangalow_id)
        
        if bangalow_no_.isalpha():
            messages.error(request, 'Please Enter a Valid Bangalow No. (at least one digit is required)')
            return redirect(bangalowFetchFun,bangalow_id)

        if len(bangalow_bhk_) <= 0:
            messages.error(request,'Please Enter Bangalow BHK !!')
            return redirect(bangalowFetchFun,bangalow_id)
        
        if len(bangalow_area_) <= 0:
            messages.error(request, "Please Enter Bangalow Area !!")
            return redirect(bangalowFetchFun,bangalow_id)
        
        if len(bangalow_price_) <= 0:
            messages.error(request, "Please Enter Bangalow Price !!")
            return redirect(bangalowFetchFun,bangalow_id)
        
        if not bangalow_price_.isdigit():
                messages.error(request, 'Please Enter A Valid Bangalow Price. (only digits are allowed)')
                return redirect(bangalowFetchFun,bangalow_id)

        if bangalow_is_active_ == None:
            active = "Off"
        else:
            active = "On"

        bangalow_data = bangalowModel.objects.get(pk=bangalow_id)
        bangalow_data.bangalow_no = bangalow_no_ 
        bangalow_data.bangalow_bHK = bangalow_bhk_
        bangalow_data.bangalow_area = bangalow_area_
        bangalow_data.bangalow_price = bangalow_price_
        bangalow_data.bangalow_is_active = active

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

        # Format the datetime object into the desired output format
        output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

        bangalow_data.bangalow_created_at_update = output_string


        bangalow_data.save()
        if bangalow_data.bangalow_id:
            messages.success(request, "Bangalow Data Update !!")
            return redirect(bangalowFetchFun,bangalow_id)
        else:
            messages.error(request, "Something goes wrong in updation!!")
            return redirect(bangalowFetchFun,bangalow_id)
    return render(request, 'Bangalow_Edit.html')

# delete record in the data in bangalowmodel_tb table
def bangalowDeleteFun(request,bangalow_id):
    if bangalowModel.objects.filter(pk=bangalow_id).exists():
        datadel = bangalowModel.objects.get(pk=bangalow_id)
        datadel.delete()
        messages.success(request, "Bangalow Data Delete succesfully!!")
    return redirect(bangalowViewFun)


# Visitor
'''
        Visitor Details (insert)
        Request : POST
        Data :{
                    "visitor_id": "Pacific_Homes_Bangalow_wq5d3s8ubye17zf",
                    "visitor_first_name" : "yash",
                    "visitor_last_name": "patel",
                    "visitor_location": "surat"
                    "visitor_email_id" = "abc@gmail.com"
                    "visitor_whatapp_phoneNo"="9759633545"
                    "visitor_phoneNo"="9759633545"
                    "visitor_is_active" = "On/Off"
                }
    '''
# add record in the data in Vision_tb table
def visitorRegisterFun(request):
    bangalow_view = bangalowModel.objects.all()
    
    if request.method == "POST":

        bangalow_ = request.POST.get('bangalowNo')
        visitor_first_name_ = request.POST.get('visitorFirstName')
        visitor_last_name_ = request.POST.get('visitorLastName')
        visitor_location_ = request.POST.get('visitorLocation')
        visitor_email_id_ = request.POST.get('visitoremail')
        visitor_whatapp_phoneNo_ = request.POST.get('visitorwhatappno')
        visitor_phoneNo_ = request.POST.get('visitorphoneno')
        visitor_is_active_ = request.POST.get('visitordisable')
        
        if len(bangalow_) == "select":
            messages.error(request, "Please select Bangalow No !!")
            return redirect(visitorRegisterFun)

        if len(visitor_first_name_) <= 0:
            messages.error(request,'Please Enter Visitor First Name & Middle Name !!')
            return redirect(visitorRegisterFun)
        # if not visitor_first_name_.isalpha():
        #         messages.error(request, 'Please Enter a Valid Visitor First Name &  Middle Name (only text characters are allowed)')
        #         return redirect(visitorRegisterFun)
        
        if len(visitor_last_name_) <= 0:
            messages.error(request,'Please Enter Visitor Last Name !!')
            return redirect(visitorRegisterFun)
        if not visitor_last_name_.isalpha():
                messages.error(request, 'Please Enter a Valid Visitor Last Name (only text characters are allowed)')
                return redirect(visitorRegisterFun)
        
        if len(visitor_location_) <= 0:
            messages.error(request,'Please Enter Visitor Location !!')
            return redirect(visitorRegisterFun)
        
        if len(visitor_email_id_) <= 0:
            messages.error(request, "Please Enter Visitor Email Id !!")
            return redirect(visitorRegisterFun)
        try:
                validate_email(visitor_email_id_)
        except ValidationError:
                messages.error(request, 'Please enter a valid email address!')
                return redirect(visitorRegisterFun)
        
        if len(visitor_whatapp_phoneNo_) <= 0:
            messages.error(request, "Please Enter Visitor Whatapp PhoneNo !!")
            return redirect(visitorRegisterFun)
        if not visitor_whatapp_phoneNo_.isdigit():
                messages.error(request, 'Please Enter a Valid Visitor Whatapp Phone No.(only digits are allowed)')
                return redirect(visitorRegisterFun)
        
        if len(visitor_phoneNo_) <= 0:
            messages.error(request, "Please Enter Visitor PhoneNo !!")
            return redirect(visitorRegisterFun)
        if not visitor_phoneNo_.isdigit():
                messages.error(request, 'Please Enter a Valid Visitor Phone No.(only digits are allowed)')
                return redirect(visitorRegisterFun)

        if visitor_is_active_ == None:
            active = "Off"
        else:
            active = "On" 


        randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        uniqueID = "Pacific_Homes_Bangalow_" + randomstr

        bangalowinstance = bangalowModel.objects.get(pk=bangalow_)
    
        bangalow = visitorModel(
            visitor_id = uniqueID,
            bangalow = bangalowinstance,
            visitor_first_name = visitor_first_name_,
            visitor_last_name = visitor_last_name_ ,
            visitor_location = visitor_location_,
            visitor_email_id = visitor_email_id_,
            visitor_whatapp_phoneNo = visitor_whatapp_phoneNo_,
            visitor_phoneNo = visitor_phoneNo_,
            visitor_is_active = active
        )

        bangalow.save()

        if bangalow.visitor_id:
            messages.success(request, "Visitor Data is add succesfully!!")
            return redirect(visitorRegisterFun)
        else:
            messages.error(request, "Something is wrong!!")
            return redirect(visitorRegisterFun)
    
    return render(request, 'Visitor_Add.html',{"bangalow_view":bangalow_view})

# View record in the data in Vision_tb table 
def visitorViewFun(request):
    visitor_view = visitorModel.objects.all()
    return render(request, 'Visitor_View_Table.html',{"visitor_view": visitor_view})

# Featch the data for particular id and dispaly all data in html page
def visitorViewdetailsFun(request,visitor_id):
    visitor_details = visitorModel.objects.get(pk=visitor_id)
    return render(request, 'Visitor_View_Details.html',{'visitor_details':visitor_details})

# Featch the data for particular id and dispaly all data in html page
def visitorFetchFun(request,visitor_id):
    visitor_featch = visitorModel.objects.get(pk=visitor_id)
    bangalow_details = bangalowModel.objects.all() 
    context = {
        "visitor_featch":visitor_featch,
        "bangalow_details":bangalow_details,
    }
    return render(request, 'Visitor_Edit.html',context)

'''
        Visitor Details (Edit)
        Request : POST
        Data :{
                    "visitor_id": "Pacific_Homes_Bangalow_wq5d3s8ubye17zf",
                    "visitor_first_name" : "yash",
                    "visitor_last_name": "patel",
                    "visitor_location": "surat"
                    "Email_Id" = "abc@gmail.com"
                    "visitor_whatapp_phoneNo"="9759633545"
                    "visitor_phoneNo"="9759633545"
                    "visitor_is_active" = "On/Off"
                }
    '''
# Edit the data for particular id and dispaly all data in html page
def visitorEditFun(request):
    if request.method == 'POST':
    # Get data from the form
        visitor_id = request.POST.get('visitor_id')
        bangalow_ = request.POST.get('bangalowNo')
        visitor_first_name_ = request.POST.get('visitorFirstName')
        visitor_last_name_ = request.POST.get('visitorLastName')
        visitor_location_ = request.POST.get('visitorLocation')
        email_id = request.POST.get('visitoremail')
        visitor_whatapp_phoneNo_ = request.POST.get('visitorwhatappno')
        visitor_phoneNo_ = request.POST.get('visitorphoneno')
        visitor_is_active_ = request.POST.get('visitordisable')

        if len(bangalow_) == "select":
            messages.error(request, "Please select Bangalow No !!")
            return redirect(visitorFetchFun,visitor_id)

        if len(visitor_first_name_) <= 0:
            messages.error(request,'Please Enter Visitor First Name !!')
            return redirect(visitorFetchFun,visitor_id)
        # if not visitor_first_name_.isalpha():
        #         messages.error(request, 'Please Enter a Valid Visitor First Name &  Middle Name (only text characters are allowed)')
        #         return redirect(visitorFetchFun,visitor_id)
        
        if len(visitor_last_name_) <= 0:
            messages.error(request,'Please Enter Visitor Last Name !!')
            return redirect(visitorFetchFun,visitor_id)
        if not visitor_last_name_.isalpha():
                messages.error(request, 'Please enter a Valid Visitor Last Name (only text characters are allowed)')
                return redirect(visitorFetchFun,visitor_id)
        
        if len(visitor_location_) <= 0:
            messages.error(request,'Please Enter Visitor Location !!')
            return redirect(visitorFetchFun,visitor_id)
        
        if len(email_id) <= 0:
            messages.error(request, "Please Enter Visitor Email Id !!")
            return redirect(visitorFetchFun,visitor_id)
        try:
                validate_email(email_id)
        except ValidationError:
                messages.error(request, 'Please enter a valid email address!')
                return redirect(visitorFetchFun,visitor_id)
        
        if len(visitor_whatapp_phoneNo_) <= 0:
            messages.error(request, "Please Enter Visitor Whatapp PhoneNo !!")
            return redirect(visitorFetchFun,visitor_id)
        if not visitor_whatapp_phoneNo_.isdigit():
                messages.error(request, 'Please Enter a Valid Visitor Whatapp Phone No.(only digits are allowed)')
                return redirect(visitorFetchFun,visitor_id)
        
        if len(visitor_phoneNo_) <= 0:
            messages.error(request, "Please Enter Visitor PhoneNo !!")
            return redirect(visitorFetchFun,visitor_id)
        if not visitor_phoneNo_.isdigit():
                messages.error(request, 'Please Enter a Valid Visitor Phone No.(only digits are allowed)')
                return redirect(visitorFetchFun,visitor_id)

        if visitor_is_active_ == None:
            active = "Off"
        else:
            active = "On" 

        
        
        bangalowinstance = bangalowModel.objects.get(bangalow_no=bangalow_)
        
        visitor_data = visitorModel.objects.get(pk=visitor_id)

        visitor_data.bangalow = bangalowinstance
        visitor_data.visitor_first_name = visitor_first_name_
        visitor_data.visitor_last_name= visitor_last_name_ 
        visitor_data.visitor_location = visitor_location_
        visitor_data.visitor_email_id = email_id
        visitor_data.visitor_whatapp_phoneNo = visitor_whatapp_phoneNo_
        visitor_data.visitor_phoneNo = visitor_phoneNo_
        visitor_data.visitor_is_active = active
        

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

        # Format the datetime object into the desired output format
        output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

        visitor_data.visitor_created_at_update = output_string


        visitor_data.save()
        if visitor_data.visitor_id:
            messages.success(request, "Visitor Data Update !!")
            return redirect(visitorFetchFun,visitor_id)
        else:
            messages.error(request, "Something goes wrong in updation!!")
            return redirect(visitorFetchFun,visitor_id)
    return render(request, 'Visitor_Edit.html')

# delete record in the data in Visitor_tb table
def visitorDeleteFun(request,visitor_id):
    if visitorModel.objects.filter(pk=visitor_id).exists():
        datadel = visitorModel.objects.get(pk=visitor_id)
        datadel.delete()
        messages.success(request, "Visitor Data Delete succesfully!!")
    return redirect(visitorViewFun)


# Client
'''
        Client Details (insert)
        Request : POST
        Data :{
                    "client_id": "Pacific_Homes_Bangalow_wq5d3s8ubye17zf",
                    "client_bangalow_no" : "103",
                    "client_first_name" : "mansukhbhai",
                    "client_last_name" : "kakadiya",
                    "client_aadhar_card_no": "1256547896",
                    "client_proof": "abs.pdf",
                    "client_total_price" = "63 Lakh",
                    "client_total_cash_price"="5,00,000",
                    "client_total_loan_price"="58,00,000",
                    "client_is_active" = "On/Off"
                }
    '''

def clientdatafetchFun(request, visitor_id):
    try:
        # Assuming visitor_id is the primary key in your model
        selected_visitor = visitorModel.objects.get(visitor_id=visitor_id)

        # Build the data dictionary based on the fields you want to retrieve
        data = {
            'visitor_id': selected_visitor.visitor_id,
            'visitor_banglow': selected_visitor.bangalow.bangalow_no,
            'visitor_first_name': selected_visitor.visitor_first_name,
            'visitor_last_name': selected_visitor.visitor_last_name,
            'visitor_email_id': selected_visitor.visitor_email_id,
            'visitor_phoneNo': selected_visitor.visitor_phoneNo,
            # Add more fields as needed
        }
        return JsonResponse(data)
    except visitorModel.DoesNotExist:
        return JsonResponse({'error': 'Visitor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# add record in the data in Client_tb table
def clientRegisterFun(request):
    visitor_view = visitorModel.objects.all()
    if request.method == "POST":
        
        visitor_ = request.POST.get('visitormodel')
        client_bangalow_no_ = request.POST.get('clientBangalowNo')
        client_phone_no_ = request.POST.get('clientPhoneNo')
        client_first_name_ = request.POST.get('clientFirstName')
        client_last_name_ = request.POST.get('clientLastName')
        client_email_id_ = request.POST.get('clientemail')
        client_aadhar_card_no_ = request.POST.get('clientAadharCardNo')
        client_pan_card_no_ = request.POST.get('clientPanCardNo')
        client_proof_ = request.FILES.get('clientProof', None)
        client_total_price_ = request.POST.get('clientTotalPrice')
        client_amount_mode_ = request.POST.get('clientAmountMode')
        client_transition_ = request.POST.get('clientTransition')
        client_token_payment_ = request.POST.get('clientTokenPayment')
        client_total_remaining_amount_ = request.POST.get('clientTotalRemainingAmount')
        client_time_period_ = request.POST.get('clientTimePeriod')
        client_monthly_amount_ = request.POST.get('clientMonthlyAmount')
        client_date_ = request.POST.get('clientDate')
        client_is_active_ = request.POST.get('clientdisable')
        
        
        if clientModel.objects.filter(client_bangalow_no=client_bangalow_no_).exists():
            messages.error(request,'Bangalow No is already existed!!')
            return redirect(clientRegisterFun)
        
        if client_bangalow_no_.isalpha():
            messages.error(request, 'Please Enter a Valid Bangalow No. (at least one digit is required)')
            return redirect(clientRegisterFun)
        
        if (client_phone_no_) == "select":
            messages.error(request,'Please Enter Client Phone No !!')
            return redirect(clientRegisterFun)
        
        # if not client_phone_no_.isdigit():
        #         messages.error(request, 'Please Enter a Valid Client Phone No.(only digits are allowed)')
        #         return redirect(clientRegisterFun)
        
        if len(client_first_name_) <=0:
            messages.error(request,'Please Enter Client First Name &  Middle Name !!')
            return redirect(clientRegisterFun)
        # if not client_first_name_.isalpha():
        #         messages.error(request, 'Please Enter a Valid Client First Name &  Middle Name (only text characters are allowed)')
        #         return redirect(clientRegisterFun)
        
        if len(client_last_name_) <= 0:
            messages.error(request,'Please Enter Client Last Name !!')
            return redirect(clientRegisterFun)
        if not client_last_name_.isalpha():
                messages.error(request, 'Please Enter a Valid Client Last Name (only text characters are allowed)')
                return redirect(clientRegisterFun)
            
        if len(client_email_id_) <= 0:
            messages.error(request,'Please Enter Client Email !!')
            return redirect(clientRegisterFun)
        try:
                validate_email(client_email_id_)
        except ValidationError:
                messages.error(request, 'Please Enter a valid email address!')
                return redirect(clientRegisterFun)
        
        if len(client_aadhar_card_no_) <= 0:
            messages.error(request,'Please Enter Client Adhar Card No. !!')
            return redirect(clientRegisterFun)
        if not client_aadhar_card_no_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Aadhar Card No.(only digits are allowed)')
                return redirect(clientRegisterFun)
        
        if len(client_pan_card_no_) <= 0:
            messages.error(request, "Please Enter Client Pan Card No. !!")
            return redirect(clientRegisterFun)
        
        if len(client_total_price_) <= 0:
            messages.error(request, "Please Enter Client Total Price !!")
            return redirect(clientRegisterFun)
        
        if not client_total_price_.isdigit():
                messages.error(request, 'Please Enter A Valid Total Price. (only digits are allowed)')
                return redirect(clientRegisterFun)
        
        if (client_amount_mode_) == "select":
            messages.error(request, "Please Enter Client Amount Mode !!")
            return redirect(clientRegisterFun)
        
        if len(client_transition_) == "select":
            messages.error(request, "Please Enter Client Transition !!")
            return redirect(clientRegisterFun)
        
        if len(client_token_payment_) <= 0:
            messages.error(request, "Please Enter Client Transition Payment !!")
            return redirect(clientRegisterFun)
        
        if not client_token_payment_.isdigit():
                messages.error(request, 'Please Enter A Valid Token Price. (only digits are allowed)')
                return redirect(clientRegisterFun)
        
        if len(client_total_remaining_amount_) <= 0:
            messages.error(request, "Please Enter Client Total Remaining Amount !!")
            return redirect(clientRegisterFun)
        
        if not client_total_remaining_amount_.isdigit():
                messages.error(request, 'Please Enter A Valid Total Remaining Amount. (only digits are allowed)')
                return redirect(clientRegisterFun)
        
        if len(client_time_period_) == "select":
            messages.error(request, "Please Enter Client Time Period !!")
            return redirect(clientRegisterFun)
        
        if len(client_monthly_amount_) <= 0:
            messages.error(request, "Please Enter Client Monthly Amount !!")
            return redirect(clientRegisterFun)
        
        
        
        if len(client_date_) <= 0:
            messages.error(request, "Please Enter Client date !!")
            return redirect(clientRegisterFun)
        try:
            # Try to parse the date with the expected format (2-12-2023)
            output_client_date_ = datetime.strptime(client_date_, "%d-%m-%Y").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use DD-MM-YYYY.")
            return redirect(clientRegisterFun)
        
        if client_is_active_ == None:
            active = "Off"
        else:
            active = "On"
        
        # if not (client_proof_.name.endswith(".pdf")):
        #     messages.error(request, "Please Select Client Proof .pdf !!")
        #     return redirect(clientRegisterFun)
        fs = FileSystemStorage()
        
        fs.save("Pacific_Homes/Client_Proof/" + client_proof_.name, client_proof_)

        randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        uniqueID = "Pacific_Homes_Bangalow_" + randomstr

        # bangalowinstance = bangalowModel.objects.get(pk=bangalow_)
        visitorinstance = visitorModel.objects.get(pk = visitor_)
    
        client = clientModel(
            client_id = uniqueID,
            visitor = visitorinstance,
            client_bangalow_no =client_bangalow_no_,
            client_phone_no = visitorinstance.visitor_whatapp_phoneNo,
            client_first_name = client_first_name_,
            client_last_name = client_last_name_,
            client_email_id = client_email_id_,
            client_aadhar_card_no = client_aadhar_card_no_,
            client_pan_card_no = client_pan_card_no_,
            client_total_price = client_total_price_ ,
            client_amount_mode = client_amount_mode_,
            client_transition = client_transition_,
            client_token_payment = client_token_payment_,
            client_total_remaining_amount = client_total_remaining_amount_ ,
            client_time_period = client_time_period_,
            client_monthly_amount = client_monthly_amount_,
            client_date = output_client_date_,
            client_proof ="media/Pacific_Homes/Client_Proof/" + client_proof_.name,
            client_is_active = active
        )

        client.save()

        if client.client_id:
            messages.success(request, "Client Data is add succesfully!!")
            return redirect(clientRegisterFun)
        else:
            messages.error(request, "Something is wrong!!")
            return redirect(clientRegisterFun)
        
    
    return render(request, 'Client_Add.html',{"visitor_view":visitor_view})

# View record in the data in Client_tb table 
def clientViewFun(request):
    client_view = clientModel.objects.all()
    return render(request, 'Client_View_Table.html',{"client_view": client_view})

# Featch the data for particular id and dispaly all data in html page
def clientViewdetailsFun(request,client_id):
    client_details = clientModel.objects.get(pk=client_id)
    return render(request, 'Client_View_Details.html',{'client_details':client_details})

# Featch the data for particular id and dispaly all data in html page
def clientFetchFun(request,client_id):
    client_featch = clientModel.objects.get(pk=client_id)
    visitor_details = visitorModel.objects.all() 
    context = {
        "client_featch":client_featch,
        "visitor_details":visitor_details,
    }
    return render(request, 'Client_Edit.html',context)

'''
        Client Details (Edit)
        Request : POST
        Data :{
                    "client_id": "Pacific_Homes_Bangalow_wq5d3s8ubye17zf",
                    "client_bangalow_no" : "103",
                    "client_first_name" : "mansukhbhai",
                    "client_last_name" : "kakadiya",
                    "client_phone_no" : "12365479",
                    "client_bhk" : "2bhk/3bhk",
                    "client_aadhar_card_no": "1256547896",
                    "client_proof": "abs.pdf",
                    "client_total_price" = "63 Lakh",
                    "client_total_cash_price"="5,00,000",
                    "client_total_loan_price"="58,00,000",
                    "client_is_active" = "On/Off"
                }
    '''
# Edit the data for particular id and dispaly all data in html page
def clientEditFun(request):
    if request.method == 'POST':
    # Get data from the form
        client_id = request.POST.get('client_id')
        visitor_ = request.POST.get('visitormodel')
        client_bangalow_no_ = request.POST.get('clientBangalowNo')
        client_phone_no_ = request.POST.get('clientPhoneNo')
        client_first_name_ = request.POST.get('clientFirstName')
        client_last_name_ = request.POST.get('clientLastName')
        client_email_id_ = request.POST.get('clientemail')
        client_aadhar_card_no_ = request.POST.get('clientAadharCardNo')
        client_pan_card_no_ = request.POST.get('clientPanCardNo')
        client_proof_ = request.FILES.get('clientProof', None)
        client_total_price_ = request.POST.get('clientTotalPrice')
        client_amount_mode_ = request.POST.get('clientAmountMode')
        client_transition_ = request.POST.get('clientTransition')
        client_token_payment_ = request.POST.get('clientTokenPayment')
        client_total_remaining_amount_ = request.POST.get('clientTotalRemainingAmount')
        client_time_period_ = request.POST.get('clientTimePeriod')
        client_monthly_amount_ = request.POST.get('clientMonthlyAmount')
        client_date_ = request.POST.get('clientDate')
        client_is_active_ = request.POST.get('clientdisable')
        
        if len(client_bangalow_no_) <=0:
            messages.error(request, "Please Enter Bangalow No !!")
            return redirect(clientFetchFun,client_id)
        
        if client_bangalow_no_.isalpha():
            messages.error(request, 'Please Enter a Valid Bangalow No. (at least one digit is required)')
            return redirect(clientFetchFun,client_id)
        
        if len(client_phone_no_) <=0:
            messages.error(request,'Please Enter Client Phone No. !!')
            return redirect(clientFetchFun,client_id)
        
        if not client_phone_no_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Phone No.(only digits are allowed)')
                return redirect(clientFetchFun,client_id)

        if len(client_first_name_) <=0:
            messages.error(request,'Please Enter First Name !!')
            return redirect(clientFetchFun,client_id)
        # if not client_first_name_.isalpha():
        #         messages.error(request, 'Please Enter a Valid Client First Name &  Middle Name (only text characters are allowed)')
        #         return redirect(clientFetchFun,client_id)
        
        if len(client_last_name_) <= 0:
            messages.error(request,'Please Enter Last Name !!')
            return redirect(clientFetchFun,client_id)
        if not client_last_name_.isalpha():
                messages.error(request, 'Please Enter a Valid Client Last Name (only text characters are allowed)')
                return redirect(clientFetchFun,client_id)
        
        if len(client_email_id_) <=0:
            messages.error(request,'Please Enter Email !!')
            return redirect(clientFetchFun,client_id)
        try:
                validate_email(client_email_id_)
        except ValidationError:
                messages.error(request, 'Please Enter a valid email address!')
                return redirect(clientFetchFun,client_id)
        
        if len(client_aadhar_card_no_) <= 0:
            messages.error(request,'Please Enter Client Adhar Card No. !!')
            return redirect(clientFetchFun,client_id)
        if not client_aadhar_card_no_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Aadhar Card No.(only digits are allowed)')
                return redirect(clientFetchFun,client_id)
        
        if len(client_pan_card_no_) <= 0:
            messages.error(request, "Please Enter Client Pan Card No. !!")
            return redirect(clientFetchFun,client_id)
        
        if len(client_total_price_) <= 0:
            messages.error(request, "Please Enter Client Total Price !!")
            return redirect(clientFetchFun,client_id)
        
        if len(client_amount_mode_) <= 0:
            messages.error(request, "Please Enter Client Amount Mode !!")
            return redirect(clientFetchFun,client_id)
        
        if len(client_transition_) <= 0:
            messages.error(request, "Please Enter Client Transition !!")
            return redirect(clientFetchFun,client_id)
        
        if len(client_token_payment_) <= 0:
            messages.error(request, "Please Enter Client Transition Payment !!")
            return redirect(clientFetchFun,client_id)
        
        if len(client_total_remaining_amount_) <= 0:
            messages.error(request, "Please Enter Client Total Remaining Amount !!")
            return redirect(clientFetchFun,client_id)
        
        if len(client_time_period_) <= 0:
            messages.error(request, "Please Enter Client Time Period !!")
            return redirect(clientFetchFun,client_id)
        
        if len(client_monthly_amount_) <= 0:
            messages.error(request, "Please Enter Client Monthly Amount !!")
            return redirect(clientFetchFun,client_id)
        
        if len(client_date_) <= 0:
            messages.error(request, "Please Enter Client date !!")
            return redirect(clientFetchFun,client_id)
        
        
        if client_is_active_ == None:
            active = "Off"
        else:
            active = "On"
        
        
        visitorinstance = visitorModel.objects.get(visitor_whatapp_phoneNo = client_phone_no_)
        
        client_data = clientModel.objects.get(pk=client_id)

        client_data.visitor = visitorinstance
        client_data.client_bangalow_no = client_bangalow_no_
        client_data.client_phone_no = client_phone_no_
        client_data.client_first_name = client_first_name_
        client_data.client_last_name = client_last_name_
        client_data.client_email_id = client_email_id_
        client_data.client_aadhar_card_no = client_aadhar_card_no_
        client_data.client_pan_card_no = client_pan_card_no_
        client_data.client_total_price = client_total_price_ 
        client_data.client_amount_mode = client_amount_mode_
        client_data.client_transition = client_transition_
        client_data.client_token_payment = client_token_payment_
        client_data.client_total_remaining_amount = client_total_remaining_amount_
        client_data.client_time_period = client_time_period_
        client_data.client_monthly_amount = client_monthly_amount_
        client_data.client_date = client_date_
        client_data.client_is_active = active
        
        fs = FileSystemStorage()
        if client_proof_:
            # Save and validate image
            fs.save("Pacific_Homes/Client_Proof/" + client_proof_.name, client_proof_)
            clientproofupdate = "media/Pacific_Homes/Client_Proof/" + client_proof_.name            
        else:
            clientproofupdate = client_data.client_proof
        client_data.client_proof = clientproofupdate

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

        # Format the datetime object into the desired output format
        output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

        client_data.client_created_at_update = output_string


        client_data.save()
        if client_data.client_id:
            messages.success(request, "Client Data Update !!")
            return redirect(clientFetchFun,client_id)
        else:
            messages.error(request, "Something goes wrong in updation!!")
            return redirect(clientFetchFun,client_id)
    return render(request, 'Client_Edit.html')

# delete record in the data in Client_tb table
def clientDeleteFun(request,client_id):
    if clientModel.objects.filter(pk=client_id).exists():
        datadel = clientModel.objects.get(pk=client_id)
        datadel.delete()
        messages.success(request, "Client Data Delete succesfully!!")
    return redirect(clientViewFun)


# Money Management
# client data fetch moneymanagement Page Using Javascript & Ajax
def moneyManagementdatafetchFun(request, client_id):
    try:
        # Assuming client_id is the primary key in your model
        selected_cilent = clientModel.objects.get(client_id=client_id)
        try:
            selected_remaing_amount = moneyManagementModel.objects.filter(moneyManagement_bangalow_no=selected_cilent.client_bangalow_no).order_by('moneyManagement_date').last()
        # Build the data dictionary based on the fields you want to retrieve
        except:
             selected_remaing_amount = None
        if selected_remaing_amount :
            data = {
                'client_id': selected_cilent.client_id,
                'client_bangalow_no': selected_cilent.client_bangalow_no,
                'client_phone_no': selected_cilent.visitor.visitor_whatapp_phoneNo,
                'client_total_price': selected_cilent.client_total_price,
                'client_token_payment': selected_cilent.client_token_payment,
                'client_total_remaining_amount': selected_remaing_amount.moneyManagement_remaining_Payment,
                'client_monthly_amount': selected_cilent.client_monthly_amount,
                # Add more fields as needed
            }
        else :
            data = {
                'client_id': selected_cilent.client_id,
                'client_bangalow_no': selected_cilent.client_bangalow_no,
                'client_phone_no': selected_cilent.visitor.visitor_whatapp_phoneNo,
                'client_total_price': selected_cilent.client_total_price,
                'client_token_payment': selected_cilent.client_token_payment,
                'client_total_remaining_amount': selected_cilent.client_total_remaining_amount,
                'client_monthly_amount': selected_cilent.client_monthly_amount,
                # Add more fields as needed
            }
        
        return JsonResponse(data)
    except visitorModel.DoesNotExist:
        return JsonResponse({'error': 'Visitor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Money Management Page Show Table
def moneyManagementtablefetchFun(request, client_id):
    
    selected_client = clientModel.objects.get(client_id=client_id)
    selected_banglows = moneyManagementModel.objects.filter(moneyManagement_bangalow_no=selected_client.client_bangalow_no)

    # Build the data dictionary based on the fields you want to retrieve
    data = {
        'entries': []
    }

    # Add transaction details to the data dictionary
    clientdata = {
            'moneyManagement_amount_mode' : selected_client.client_amount_mode,
            'moneyManagement_total_amount': selected_client.client_total_price,
            'moneyManagement_installment_amount': selected_client.client_token_payment,
            'moneyManagement_transition': selected_client.client_transition,
            'moneyManagement_remaining_Payment': selected_client.client_total_remaining_amount,
            'moneyManagement_date': selected_client.client_date,
        }
    
    data['entries'].append(clientdata)

    for selected_banglow in selected_banglows:
        selected_banglow_data = {
            'moneyManagement_id': selected_banglow.moneyManagement_id,
            'moneyManagement_amount_mode': selected_banglow.moneyManagement_amount_mode,
            'moneyManagement_total_amount': selected_banglow.moneyManagement_total_amount,
            'moneyManagement_installment_amount': selected_banglow.moneyManagement_installment_amount,
            'moneyManagement_transition': selected_banglow.moneyManagement_transition,
            'moneyManagement_remaining_Payment': selected_banglow.moneyManagement_remaining_Payment,
            'moneyManagement_date': selected_banglow.moneyManagement_date,  # Format the date as needed
        }
        
        data['entries'].append(selected_banglow_data)


    return JsonResponse(data)

'''
        Money Management Details (insert)
        Request : POST
        Data :{
                    "moneyManagement_id": "Pacific_Homes_Bangalow_wq5d3s8ubye17zf",
                    "moneyManagement_amount_mode ="token/downpyment",
                    "moneyManagement_amount_payment = "2,00,000",
                    "moneyManagement_amount_transition = "loan/cash",
                    "moneyManagement_total_remaining_amount =  "54,00,000",
                    "moneyManagement_remaining_loan_amount = "50,00,000",
                    "moneyManagement_remaining_cash_amount = "4,00,000",
                    "moneyManagement_date ="29/11/2023",
                    "moneyManagement_bank_name = "BOB",
                    "moneyManagement_bank_branch = "Adajan",
                    "moneyManagement_IFSE_No =  "896355545",
                    "moneyManagement_cheque_No = "96359",
                    "moneyManagement_cheque_Ac_No = "9563",
                    "moneyManagement_transition_proof ="img",
                    "moneyManagement_cheque_photo ="img",
                    "moneyManagement_is_active = "On/Off"
                    
                }
    '''
# add record in the data in moneymanagementmodel_tb table
def moneyManagementRegisterFun(request):
    client_view = clientModel.objects.all()
    if request.method == "POST":

        client_ = request.POST.get('clientBangalowNo')
        moneyManagement_bangalow_no_ = request.POST.get('moneyManagementBangalowNo')
        moneyManagement_phone_no_ = request.POST.get('moneyManagementPhoneNo')
        moneyManagement_total_amount_ = request.POST.get('moneyManagementTotalAmount')
        moneyManagement_token_amount_ = request.POST.get('moneyManagementTokenAmount')
        moneyManagement_total_remaining_amount_ = request.POST.get('moneyManagementTotalRemainingAmount')
        moneyManagement_amount_mode_ = request.POST.get('moneyManagementAmountMode')
        moneyManagement_transition_ = request.POST.get('moneyManagementTransition')
        moneyManagement_installment_amount_ = request.POST.get('moneyManagementInstallmentAmount')
        moneyManagement_remaining_Payment_ = request.POST.get('moneyManagementRemainingPayment')
        moneyManagement_date_ = request.POST.get('moneyManagementDate')
        moneyManagement_transition_proof_ = request.FILES.get('moneyManagementTransitionProof', False) 
        moneyManagement_cheque_photo_ = request.FILES.get('moneyManagementChequePhoto', False)
        moneyManagement_bank_name_ = request.POST.get('moneyManagementBankName')
        moneyManagement_bank_branch_ = request.POST.get('moneyManagementBankBranch')
        moneyManagement_IFSE_No_ = request.POST.get('moneyManagementIFSENo')
        moneyManagement_cheque_No_ = request.POST.get('moneyManagementChequeNo')
        moneyManagement_Account_No_ = request.POST.get('moneyManagementAccountNo')
        moneyManagement_is_active_ = request.POST.get('moneyManagementdisable')
        
        if (moneyManagement_bangalow_no_) == "select":
            messages.error(request,"Please Enter Bangalow No !!")
            return redirect(moneyManagementRegisterFun)
        
        if (moneyManagement_phone_no_) == "select":
            messages.error(request, "Please Enter Money Management Phone No !!")
            return redirect(moneyManagementRegisterFun)
        
        # if not moneyManagement_phone_no_.isdigit():
        #         messages.error(request, 'Please Enter a Valid Client Phone No.(only digits are allowed)')
        #         return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_total_amount_) <= 0:
            messages.error(request, "Please Enter Money Management Total Amount !!")
            return redirect(moneyManagementRegisterFun)
        if not moneyManagement_total_amount_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Total Amount (only digits are allowed)')
                return redirect(moneyManagementRegisterFun)
        
        if (moneyManagement_amount_mode_) == "select":
            messages.error(request, "Please Select Amount Mode !!")
            return redirect(moneyManagementRegisterFun)
        
        if (moneyManagement_transition_) == "select":
            messages.error(request, "Please Select Transition Type !!")
            return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_installment_amount_) <=0:
            messages.error(request, "Please Enter Installment Amount !!")
            return redirect(moneyManagementRegisterFun)
        
        if not moneyManagement_installment_amount_.isdigit():
                messages.error(request, 'Please Enter a Valid Client moneyManagement Installment Amount (only digits are allowed)')
                return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_remaining_Payment_) <= 0:
            messages.error(request, "Please Enter Total Remaining Amount !!")
            return redirect(moneyManagementRegisterFun)
        
        if not moneyManagement_remaining_Payment_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Remaining Payment (only digits are allowed)')
                return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_token_amount_) <= 0:
            messages.error(request, "Please Enter Token Amount !!")
            return redirect(moneyManagementRegisterFun)
        
        if not moneyManagement_token_amount_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Token Amount (only digits are allowed)')
                return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_total_remaining_amount_) <= 0:
            messages.error(request, "Please Enter Total Remaining Amount !!")
            return redirect(moneyManagementRegisterFun)
        
        if not moneyManagement_total_remaining_amount_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Remaining Amount (only digits are allowed)')
                return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_date_) <=0:
            messages.error(request, "Please Enter Money Management Date !!")
            return redirect(moneyManagementRegisterFun)
        try:
            # Try to parse the date with the expected format (2-12-2023)
            output_moneyManagement_date_ = datetime.strptime(moneyManagement_date_, "%d-%m-%Y").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use DD-MM-YYYY.")
            return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_bank_name_) <= 0:
            messages.error(request, "Please Enter Money Management Bank Name !!")
            return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_bank_branch_) <= 0:
            messages.error(request, "Please Enter Money Management Bank Branch !!")
            return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_IFSE_No_) <= 0:
            messages.error(request, "Please Enter Money Management IFSE No !!")
            return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_cheque_No_) <= 0:
            messages.error(request, "Please Enter Money Management Cheque No !!")
            return redirect(moneyManagementRegisterFun)
        
        if len(moneyManagement_Account_No_) <= 0:
            messages.error(request, "Please Enter Money Management Cheque_Ac_No !!")
            return redirect(moneyManagementRegisterFun)
        
        if not moneyManagement_transition_proof_:
            messages.error(request, "Please Money Management Transition Proof img Select")
            return redirect(moneyManagementRegisterFun)
        
        if not moneyManagement_cheque_photo_:
            messages.error(request, "Please Money Management Cheque Photo img Select")
            return redirect(moneyManagementRegisterFun)
        
        if moneyManagement_is_active_ == None:
            active = "Off"
        else:
            active = "On"

        fs = FileSystemStorage()
        
        fs.save("Pacific_Homes/Client_Transation_Photo/" + moneyManagement_transition_proof_.name, moneyManagement_transition_proof_)
        fs.save("Pacific_Homes/Client_Cheque_Photo/" + moneyManagement_cheque_photo_.name, moneyManagement_cheque_photo_)

        randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        uniqueID = "Pacific_Homes_Bangalow_" + randomstr

        # bangalowinstance = bangalowModel.objects.get(pk=bangalow_)

        clientinstance = clientModel.objects.get(pk=moneyManagement_bangalow_no_)
    
        moneyManagement = moneyManagementModel(
            moneyManagement_id = uniqueID,
            client = clientinstance,
            moneyManagement_bangalow_no = clientinstance.client_bangalow_no,
            moneyManagement_phone_no = moneyManagement_phone_no_,
            moneyManagement_total_amount = moneyManagement_total_amount_,
            moneyManagement_token_amount = moneyManagement_token_amount_,
            moneyManagement_total_remaining_amount = moneyManagement_total_remaining_amount_,
            moneyManagement_amount_mode = moneyManagement_amount_mode_,
            moneyManagement_transition = moneyManagement_transition_,
            moneyManagement_installment_amount = moneyManagement_installment_amount_,
            moneyManagement_remaining_Payment = moneyManagement_remaining_Payment_,
            moneyManagement_date = output_moneyManagement_date_,
            moneyManagement_transition_proof ="media/Pacific_Homes/Client_Transation_Photo/" + moneyManagement_transition_proof_.name,
            moneyManagement_cheque_photo ="media/Pacific_Homes/Client_Cheque_Photo/" + moneyManagement_cheque_photo_.name,
            moneyManagement_bank_name = moneyManagement_bank_name_,
            moneyManagement_bank_branch = moneyManagement_bank_branch_,
            moneyManagement_IFSE_No = moneyManagement_IFSE_No_,
            moneyManagement_cheque_No = moneyManagement_cheque_No_,
            moneyManagement_Account_No = moneyManagement_Account_No_,
            moneyManagement_is_active = active

        )

        moneyManagement.save()
        
        entries = moneyManagementModel.objects.filter(moneyManagement_bangalow_no=moneyManagement.moneyManagement_bangalow_no)
        print(entries)
        # Pass the entries to the template for rendering
        return render(request, 'Money_Management_Add.html', {"entries": entries})
        if moneyManagement.moneyManagement_id:
            messages.success(request, "Money Management Data is add succesfully!!")
            return render(request, 'Money_Management_Add.html', {"entries": entries})
            
            return redirect(moneyManagementRegisterFun)
        
        else:
            messages.error(request, "Something is wrong!!")
            return redirect(moneyManagementRegisterFun)
        
    
    return render(request, 'Money_Management_Add.html',{"client_view":client_view})

# View record in the data in moneymanagementmodel_tb table 
def moneyManagementViewFun(request):
    moneyManagement_view = moneyManagementModel.objects.all()
    return render(request, 'Money_Management_View_Table.html',{"moneyManagement_view": moneyManagement_view})

# Featch the data for particular id and dispaly all data in html page
def moneyManagementViewdetailsFun(request,moneyManagement_id):
    moneyManagement_details = moneyManagementModel.objects.get(pk=moneyManagement_id)
    moneygetdata = moneyManagementModel.objects.filter(moneyManagement_bangalow_no = moneyManagement_details.moneyManagement_bangalow_no)
    moneyManagement_transition_proof_image =  media_path + moneyManagement_details.moneyManagement_transition_proof
    moneyManagement_cheque_image = media_path + moneyManagement_details.moneyManagement_cheque_photo
    return render(request, 'Money_Management_View_Details.html',{'moneygetdata':moneygetdata,'moneyManagement_details':moneyManagement_details,"proof_img":moneyManagement_transition_proof_image,"cheque_img":moneyManagement_cheque_image})

# Featch the data for particular id and dispaly all data in html page
def moneyManagementFetchFun(request,moneyManagement_id):
    moneyManagement_featch = moneyManagementModel.objects.get(pk=moneyManagement_id)
    client_details = clientModel.objects.all()
    moneygetdata = moneyManagementModel.objects.filter(moneyManagement_bangalow_no = moneyManagement_featch.moneyManagement_bangalow_no)
    moneyManagement_transition_proof_image =  media_path + moneyManagement_featch.moneyManagement_transition_proof
    moneyManagement_cheque_image = media_path + moneyManagement_featch.moneyManagement_cheque_photo
    return render(request, 'Money_Management_Edit.html',{'moneygetdata':moneygetdata,"proof_img":moneyManagement_transition_proof_image,"cheque_img":moneyManagement_cheque_image,"client_details":client_details,"moneyManagement_featch":moneyManagement_featch})

'''
        Money Management Details (Edit)
        Request : POST
        Data :{
                    "moneyManagement_id": "Pacific_Homes_Bangalow_wq5d3s8ubye17zf",
                    "moneyManagement_amount_mode ="token/downpyment",
                    "moneyManagement_transition = "2,00,000",
                    "moneyManagement_installment_amount = "loan/cash",
                    "moneyManagement_remaining_Payment =  "54,00,000",
                    "moneyManagement_token_amount = "50,00,000",
                    "moneyManagement_total_remaining_amount = "4,00,000",
                    "moneyManagement_date ="29/11/2023",
                    "moneyManagement_bank_name = "BOB",
                    "moneyManagement_bank_branch = "Adajan",
                    "moneyManagement_IFSE_No =  "896355545",
                    "moneyManagement_cheque_No = "96359",
                    "moneyManagement_Account_No = "9563",
                    "moneyManagement_transition_proof ="img",
                    "moneyManagement_cheque_photo ="img",
                    "moneyManagement_is_active = "On/Off"
                    
                }
    '''
# Edit the data for particular id and dispaly all data in html page
def moneyManagementEditFun(request):
    if request.method == 'POST':
    # Get data from the form
        moneyManagement_id = request.POST.get('moneyManagement_id')
        client_ = request.POST.get('clientBangalowNo')
        moneyManagement_bangalow_no_ = request.POST.get('moneyManagementBangalowNo')
        moneyManagement_phone_no_ = request.POST.get('moneyManagementPhoneNo')
        moneyManagement_total_amount_ = request.POST.get('moneyManagementTotalAmount')
        moneyManagement_token_amount_ = request.POST.get('moneyManagementTokenAmount')
        moneyManagement_total_remaining_amount_ = request.POST.get('moneyManagementTotalRemainingAmount')
        moneyManagement_amount_mode_ = request.POST.get('moneyManagementAmountMode')
        moneyManagement_transition_ = request.POST.get('moneyManagementTransition')
        moneyManagement_installment_amount_ = request.POST.get('moneyManagementInstallmentAmount')
        moneyManagement_remaining_Payment_ = request.POST.get('moneyManagementRemainingPayment')
        moneyManagement_date_ = request.POST.get('moneyManagementDate')
        moneyManagement_bank_name_ = request.POST.get('moneyManagementBankName')
        moneyManagement_bank_branch_ = request.POST.get('moneyManagementBankBranch')
        moneyManagement_IFSE_No_ = request.POST.get('moneyManagementIFSENo')
        moneyManagement_cheque_No_ = request.POST.get('moneyManagementChequeNo')
        moneyManagement_Account_No_ = request.POST.get('moneyManagementAccountNo')
        moneyManagement_is_active_ = request.POST.get('moneyManagementdisable')
        
        if (moneyManagement_bangalow_no_) == "select":
            messages.error(request,"Please Enter Bangalow No !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if (moneyManagement_phone_no_) == "select":
            messages.error(request, "Please Enter Money Management Phone No !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        # if not moneyManagement_phone_no_.isdigit():
        #         messages.error(request, 'Please Enter a Valid Client Phone No.(only digits are allowed)')
        #         return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_total_amount_) <= 0:
            messages.error(request, "Please Enter Money Management Total Amount !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        if not moneyManagement_total_amount_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Total Amount (only digits are allowed)')
                return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if (moneyManagement_amount_mode_) == "select":
            messages.error(request, "Please Select Amount Mode !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if (moneyManagement_transition_) == "select":
            messages.error(request, "Please Select Transition Type !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_installment_amount_) <=0:
            messages.error(request, "Please Enter Installment Amount !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if not moneyManagement_installment_amount_.isdigit():
                messages.error(request, 'Please Enter a Valid Client moneyManagement Installment Amount (only digits are allowed)')
                return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_remaining_Payment_) <= 0:
            messages.error(request, "Please Enter Total Remaining Amount !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if not moneyManagement_remaining_Payment_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Remaining Payment (only digits are allowed)')
                return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_token_amount_) <= 0:
            messages.error(request, "Please Enter Token Amount !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if not moneyManagement_token_amount_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Token Amount (only digits are allowed)')
                return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_total_remaining_amount_) <= 0:
            messages.error(request, "Please Enter Total Remaining Amount !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if not moneyManagement_total_remaining_amount_.isdigit():
                messages.error(request, 'Please Enter a Valid Client Remaining Amount (only digits are allowed)')
                return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_date_) <=0:
            messages.error(request, "Please Enter Money Management Date !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_bank_name_) <= 0:
            messages.error(request, "Please Enter Money Management Bank Name !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_bank_branch_) <= 0:
            messages.error(request, "Please Enter Money Management Bank Branch !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_IFSE_No_) <= 0:
            messages.error(request, "Please Enter Money Management IFSE No !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_cheque_No_) <= 0:
            messages.error(request, "Please Enter Money Management Cheque No !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if len(moneyManagement_Account_No_) <= 0:
            messages.error(request, "Please Enter Money Management Cheque_Ac_No !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        
        if moneyManagement_is_active_ == None:
            active = "Off"
        else:
            active = "On"

        moneyManagement_transition_proof_ = request.FILES.get('moneyManagementTransitionProof', False) 
        moneyManagement_cheque_photo_ = request.FILES.get('moneyManagementChequePhoto', False)
        
        
        clientinstance = clientModel.objects.get(client_bangalow_no=moneyManagement_bangalow_no_)
        
        moneyManagement_data = moneyManagementModel.objects.get(pk=moneyManagement_id)

        moneyManagement_data.client = clientinstance
        moneyManagement_data.moneyManagement_bangalow_no = moneyManagement_bangalow_no_
        moneyManagement_data.moneyManagement_phone_no = moneyManagement_phone_no_
        moneyManagement_data.moneyManagement_total_amount = moneyManagement_total_amount_
        moneyManagement_data.moneyManagement_token_amount = moneyManagement_token_amount_
        moneyManagement_data.moneyManagement_total_remaining_amount = moneyManagement_total_remaining_amount_
        moneyManagement_data.moneyManagement_amount_mode = moneyManagement_amount_mode_
        moneyManagement_data.moneyManagement_transition = moneyManagement_transition_
        moneyManagement_data.moneyManagement_installment_amount = moneyManagement_installment_amount_
        moneyManagement_data.moneyManagement_remaining_Payment = moneyManagement_remaining_Payment_
        moneyManagement_data.moneyManagement_date = moneyManagement_date_
        moneyManagement_data.moneyManagement_bank_name = moneyManagement_bank_name_
        moneyManagement_data.moneyManagement_bank_branch = moneyManagement_bank_branch_
        moneyManagement_data.moneyManagement_IFSE_No = moneyManagement_IFSE_No_
        moneyManagement_data.moneyManagement_cheque_No = moneyManagement_cheque_No_
        moneyManagement_data.moneyManagement_Account_No = moneyManagement_Account_No_
        moneyManagement_data.moneyManagement_is_active = active

        fs = FileSystemStorage()
        if moneyManagement_transition_proof_:

            fs.save("Pacific_Homes/Client_Transation_Photo/" + moneyManagement_transition_proof_.name, moneyManagement_transition_proof_)
            savetransitionimage = "media/Pacific_Homes/Client_Transation_Photo/" + moneyManagement_transition_proof_.name
            
        else:
            savetransitionimage = moneyManagement_data.moneyManagement_transition_proof

        moneyManagement_data.moneyManagement_transition_proof = savetransitionimage
        
        if moneyManagement_transition_proof_:

            fs.save("Pacific_Homes/Client_Cheque_Photo/" + moneyManagement_cheque_photo_.name, moneyManagement_cheque_photo_)
            savechequeimage = "media/Pacific_Homes/Client_Cheque_Photo/" + moneyManagement_cheque_photo_.name
            
        else:
            savechequeimage = moneyManagement_data.moneyManagement_cheque_photo 

        moneyManagement_data.moneyManagement_cheque_photo = savechequeimage

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

        # Format the datetime object into the desired output format
        output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

        moneyManagement_data.moneyManagement_created_at_update = output_string


        moneyManagement_data.save()
        entries = moneyManagementModel.objects.filter(moneyManagement_bangalow_no=moneyManagement_data.moneyManagement_bangalow_no)
        data = {
            'entries': [
                {
                    'moneyManagement_amount_mode': entry.moneyManagement_amount_mode,
                    'moneyManagement_total_amount': entry.moneyManagement_total_amount,
                    'moneyManagement_installment_amount': entry.moneyManagement_installment_amount,
                    'moneyManagement_transition': entry.moneyManagement_transition,
                    'moneyManagement_remaining_Payment': entry.moneyManagement_remaining_Payment,
                    'moneyManagement_date': entry.moneyManagement_date,
                }
                for entry in entries
            ]
        }
        return JsonResponse(data)
        if moneyManagement_data.moneyManagement_id:
            messages.success(request, "Money Management Data Update !!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
        else:
            messages.error(request, "Something goes wrong in updation!!")
            return redirect(moneyManagementFetchFun,moneyManagement_id)
    return render(request, 'Money_Management_Edit.html')

# delete record in the data in moneymanagementmodel_tb table
def moneyManagementDeleteFun(request,moneyManagement_id):
    
    if moneyManagementModel.objects.filter(pk=moneyManagement_id).exists():
        datadel = moneyManagementModel.objects.get(pk=moneyManagement_id)
        datadel.delete()
        messages.success(request, "Money Management Data Delete succesfully!!")
    return redirect(moneyManagementViewFun)


# Resume 
def resumeRegisterFun(request):

    if request.method == "POST":
        resume_full_name_ = request.POST.get('fullname')
        resume_email_ = request.POST.get('email')
        resume_headline_ = request.POST.get('headline')
        resume_phone_no_ = request.POST.get('phoneno')
        resume_address_ = request.POST.get('address')
        resume_city_ = request.POST.get('city')
        resume_education_ = request.POST.get('education')
        resume_school_ = request.POST.get('school')
        resume_date_ = request.POST.get('educationdate')
        resume_description_ = request.POST.get('educationdescription')
        resume_image_ = request.FILES.get('resumeimage', False)
        resume_project_image_ = request.FILES.get('resumeprojectimage', False)
        resume_technical_skills_ = request.POST.get('technicalskills')
        resume_soft_skills_ = request.POST.get('softskills')
        resume_language_ = request.POST.get('language')
        resume_hobby_ = request.POST.get('hobby')
        resume_is_active_ = request.POST.get('resumedisable')

        if resume_is_active_ == None:
            active = "Off"
        else:
            active = "On"

        fs = FileSystemStorage()

        fs.save("resume/" + resume_image_.name, resume_image_)
        fs.save("resume/" + resume_project_image_.name, resume_project_image_)

        randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        uniqueID = "Resume_" + randomstr

        resumedata = resumeModel(
            resume_id=uniqueID,
            resume_full_name=resume_full_name_,
            resume_email=resume_email_,
            resume_headline=resume_headline_,
            resume_phone_no=resume_phone_no_,
            resume_address=resume_address_,
            resume_city=resume_city_,
            resume_education=resume_education_,
            resume_school=resume_school_,
            resume_date=resume_date_,
            resume_description=resume_description_,
            resume_image="media/resume/" + resume_image_.name,
            resume_project_image="media/resume/" + resume_project_image_.name,
            resume_technical_skills=resume_technical_skills_,
            resume_soft_skills=resume_soft_skills_,
            resume_language=resume_language_,
            resume_hobby=resume_hobby_,
            resume_is_active=active
        )
        resumedata.save()

        response_data = {'success': True, 'message': 'Form submitted successfully'}
        return JsonResponse(response_data)

    return render(request, 'Resume_Add.html')

def resumeViewFun(request):
    resume_view = resumeModel.objects.all()
    return render(request, 'Resume_View_Table.html',{"resume_view": resume_view})

# featch the data in main category
def resumeFetchFun(request):
    print("hhhhhhhhhhhhh", )
   
    resume_id = request.POST['resume_id']
    print(resume_id)
    resumefetchdata = resumeModel.objects.filter(pk=resume_id).values()
    
    resumelist = list(resumefetchdata)
    response_resume_fetch = {"data": resumelist}
    return JsonResponse(response_resume_fetch)

# update record in the data in main category
def resumeEditFun(request):

    resume_id = request.POST['resume_id']
    resume_full_name_ = request.POST['fullname']
    resume_email_ = request.POST['email']
    resume_headline_ = request.POST['headline']
    resume_phone_no_ = request.POST['phoneno']
    resume_address_ = request.POST['address']
    resume_city_ = request.POST['city']
    resume_education_ = request.POST['education']
    resume_school_ = request.POST['school']
    resume_date_ = request.POST['educationdate']
    resume_description_ = request.POST['educationdescription']
    old_resume_image_ = request.POST['oldresumeimage']
    old_resume_project_image_ = request.POST['oldresumeprojectimage']
    resume_technical_skills_ = request.POST['technicalskills']
    resume_soft_skills_ = request.POST['softskills']
    resume_language_ = request.POST['language']
    resume_hobby_ = request.POST['hobby']
    resume_is_active_ = request.POST.get('resumedisable')
    
    if resume_is_active_ == None:
        active = "Off"
    else:
        active = "On"

    resume_image_ = request.FILES.get('resumeimage', False)
    resume_project_image_ = request.FILES.get('resumeprojectimage', False)

    resumeupdatedata = resumeModel.objects.get(pk = resume_id)
    resumeupdatedata.resume_full_name = resume_full_name_
    resumeupdatedata.resume_email = resume_email_
    resumeupdatedata.resume_headline = resume_headline_
    resumeupdatedata.resume_phone_no = resume_phone_no_
    resumeupdatedata.resume_address = resume_address_
    resumeupdatedata.resume_city = resume_city_
    resumeupdatedata.resume_education = resume_education_
    resumeupdatedata.resume_school = resume_school_
    resumeupdatedata.resume_date = resume_date_
    resumeupdatedata.resume_description = resume_description_
    resumeupdatedata.resume_technical_skills = resume_technical_skills_
    resumeupdatedata.resume_soft_skills = resume_soft_skills_
    resumeupdatedata.resume_language = resume_language_
    resumeupdatedata.resume_hobby = resume_hobby_
    resumeupdatedata.resume_is_active = active

    fs = FileSystemStorage()

    if resume_image_ != False:

        fs.save("resume/" + resume_image_.name, resume_image_)
        resumeimagesave = "media/resume/" + resume_image_.name

    else:

        resumeimagesave = old_resume_image_
    
    if resume_project_image_ != False:

        fs.save("resume/" + resume_project_image_.name, resume_project_image_)
        resumeprojectimagesave = "media/resume/" + resume_project_image_.name

    else:

        resumeprojectimagesave = old_resume_project_image_

    resumeupdatedata.resume_image = resumeimagesave
    resumeupdatedata.resume_project_image = resumeprojectimagesave #resume_project_image from model

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

    # Format the datetime object into the desired output format
    output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

    resumeupdatedata.resume_created_at_update = output_string
    resumeupdatedata.save()

    if resumeupdatedata.resume_id:
        response =  "1"
        return HttpResponse(response)
    else:
        response =  "Something goes wrong in updation"
        return HttpResponse(response)

    return HttpResponse('1')


# delete record in the data in resumemodel_tb table
def resumeDeleteFun(request):
    
    # if resumeModel.objects.filter(pk=resume_id).exists():
    #     datadel = resumeModel.objects.get(pk=resume_id)
    #     datadel.delete()
    #     messages.success(request, "Resume Data Delete succesfully!!")
    # return redirect(resumeViewFun)
    
    resume_id = request.POST['resumedeletedata']
    resumedeletedata = resumeModel.objects.filter(pk = resume_id)
    resumedeletedata.delete()

    return HttpResponse('1')
