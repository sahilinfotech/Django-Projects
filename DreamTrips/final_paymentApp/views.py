
from django.shortcuts import render, redirect
from DreamTrips import *
from final_paymentApp.models import *
from flightApp.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from userApp.models import *
from hotelApp.models import *
from django.contrib import messages
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

    
def bookingFun(request):
    context = {
        "header": "header header-theme",
        "mainheaderClass": "",
        "headerClass": "",
        "listheader": "list-buttons light",
        "alistheader": "bg-primary",
    }
    try:
        userDetails = request.session.get("userinfo")
        if userDetails:
            user_id = userDetails['user_id']
            selected_flight_id = request.session.get('selected_flight_id')
            selected_hotel_id = request.session.get('selected_hotel_id')
            selected_destination_id = request.session.get('selected_destination_id')
            print("Session variables:")
            print("User ID:", user_id)
            print("Selected flight ID:", selected_flight_id)
            print("Selected hotel ID:", selected_hotel_id)
            print("Selected destination ID:", selected_destination_id)

            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            uniqueID = "Billing_" + randomstr

            user_guest = BillingModel(
                Billing_id=uniqueID,
                Billing_user=user_id,
                Billing_destination=selected_destination_id,
                Billing_flight=selected_flight_id,
                Billing_hotel=selected_hotel_id,
            )
            user_guest.save()

            destination = DestinationModel.objects.get(Destination_id=selected_destination_id)
            destination_stay = DestinationstayModel.objects.filter(Destination=destination)

            flight = flightClassModel.objects.get(flightClass_id=selected_flight_id)
            hotel = destinationHotelModel.objects.get(destinationHotel_id=selected_hotel_id)
            check_in_date = datetime.strptime(flight.flightDetails.flightDetails_date, '%d/%m/%Y').date()
            check_out_date = datetime.strptime(flight.flightDetails.flightDetails_return_date, '%d/%m/%Y').date()
            
            stay_duration = (check_out_date - check_in_date).days
            stay_duration_night = (stay_duration - 1)

            
            hotel.images = hotel.destinationhotelimagemodel_set.first()
            
            for destinationstay in destination_stay:
                total_price = float(destinationstay.Destinationstay_price) + float(flight.flightClass_price) + float(hotel.destinationHotel_hotel_price)

            random_reviews = random.randint(1000, 5000)
            random_rating = round(random.uniform(3.0, 5.0), 1)

            random_reviews_hotel = random.randint(1000, 5000)
            random_rating_hotel = round(random.uniform(3.0, 5.0), 1)

            if 'total_price' in request.session:
                del request.session['total_price']
                print("'current_total_price' is deleted from session")
            else:
                print("'current_total_price' is not present in session")
                

            return render(request, 'booking_page.html', {"stay_duration_night":stay_duration_night,"stay_duration":stay_duration,"total_price": total_price,"destination_stay":destination_stay,"random_reviews_hotel":random_reviews_hotel,"random_rating_hotel":random_rating_hotel,"random_rating":random_rating,"random_reviews":random_reviews,"flight": flight, "hotel": hotel, "destination": destination, "userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'booking_page.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')


def bookingdetailFun(request):
    context = {
            "header" : "header header-theme",
            "mainheaderClass" : "",
            "headerClass" : "",
            "listheader" : "list-buttons light",
            "alistheader" : "bg-primary",

        }
    try:
        userDetails = request.session.get("userinfo")
        print(userDetails)
        
        if userDetails:
            if request.method == "POST":
                user_id = userDetails.get("user_id")
                userGuest_firstname_ = request.POST.get('userGuestFirstName')
                userGuest_lastname_ = request.POST.get('userGuestLastName')
                userGuest_passport_number_ = request.POST.get('userGuestPassportNumber')
                userGuest_passport_expire_ = request.POST.get('userGuestPassportExpire')
                userGuest_dateofbirth_ = request.POST.get('userGuestDateOfBirth')
                userGuest_gender_ = request.POST.get('userGuestGender')
                userGuest_nationality_ = request.POST.get('userGuestNationality')
                
                if len(userGuest_firstname_) <= 0:
                    error ='Please Enter User First Name !!'
                    return render(request, 'booking_detail.html', {"error":error, "flag" : 0})
                
                if len(userGuest_lastname_) <= 0:
                    error ='Please Enter User Last Name !!'
                    return render(request, 'booking_detail.html', {"error":error, "flag" : 0})

                if len(userGuest_passport_number_) <= 0:
                    error ='Please Enter User Passport Number !!'
                    return render(request, 'booking_detail.html', {"error":error, "flag" : 0})
                
                
                if len(userGuest_passport_expire_) <= 0:
                    error ='Please Enter User Guest Passport Expire !!'
                    return render(request, 'booking_detail.html', {"error":error, "flag" : 0})

                if len(userGuest_dateofbirth_) <= 0:
                    error ='Please Enter User Date Of Birth !!'
                    return render(request, 'booking_detail.html', {"error":error, "flag" : 0})
                
                if not userGuest_gender_:
                    error ='Please Select User Gender !!'
                    return render(request, 'booking_detail.html', {"error":error, "flag" : 0})
                
                if len(userGuest_nationality_) <= 0:
                    error ='Please Enter User Nationality !!'
                    return render(request, 'booking_detail.html', {"error":error, "flag" : 0})
                
                randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                uniqueID = "User_Guest_" + randomstr

                user_instance = SignupModel.objects.get(user_id=user_id)

                
                userGuest = userGuestModel(
                    userGuest_id = uniqueID,
                    user = user_instance,
                    userGuest_firstname = userGuest_firstname_,
                    userGuest_lastname = userGuest_lastname_,
                    userGuest_passport_number = userGuest_passport_number_,
                    userGuest_passport_expire = userGuest_passport_expire_,
                    userGuest_dateofbirth = userGuest_dateofbirth_,
                    userGuest_gender = userGuest_gender_,
                    userGuest_nationality = userGuest_nationality_,

                    
                )
            
                

                user_id = userDetails['user_id']
                selected_flight_id = request.session.get('selected_flight_id')
                selected_hotel_id = request.session.get('selected_hotel_id')
                selected_destination_id = request.session.get('selected_destination_id')

                destination = DestinationModel.objects.get(Destination_id=selected_destination_id)
                destination_stay = DestinationstayModel.objects.filter(Destination=destination)

                flight = flightClassModel.objects.get(flightClass_id=selected_flight_id)
                hotel = destinationHotelModel.objects.get(destinationHotel_id=selected_hotel_id)

                check_in_date = datetime.strptime(flight.flightDetails.flightDetails_date, '%d/%m/%Y').date()
                check_out_date = datetime.strptime(flight.flightDetails.flightDetails_return_date, '%d/%m/%Y').date()
                
                stay_duration = (check_out_date - check_in_date).days
                stay_duration_night = (stay_duration - 1)
                

                userGuest.save()
                
                if userGuest.userGuest_id:
                    # Check if 'total_price' key exists in session, if not, initialize it to 0
                    if 'total_price' not in request.session:
                        request.session['total_price'] = 0

                    for destinationstay in destination_stay:
                        # Calculate total price for each destination stay
                        total_price = float(destinationstay.Destinationstay_price) + float(flight.flightClass_price) + float(hotel.destinationHotel_hotel_price)
                        print("Total price for current destination stay:", total_price)
                        
                        # Retrieve current total price from session
                        current_total_price = float(request.session['total_price'])
                        
                        # Double the total price for the current destination stay
                        doubled_price = total_price
                        
                        # Add the doubled total price to the accumulated total price
                        current_total_price += doubled_price
                        
                        # Update session with accumulated total price
                        request.session['total_price'] = current_total_price
                        
                        
                        print("Total price after doubling:", current_total_price)

                    return render(request, 'booking_detail.html', {"stay_duration_night":stay_duration_night,"stay_duration":stay_duration,"total_price":total_price,"current_total_price":current_total_price,"destination_stay":destination_stay,"flight": flight, "hotel": hotel, "destination": destination,"userDetails": userDetails, "context": context, "flag": 1})
                else:
                    return render(request, 'booking_detail.html', {"stay_duration_night":stay_duration_night,"current_total_price":current_total_price,"stay_duration":stay_duration,"destination_stay":destination_stay,"flight": flight, "hotel": hotel, "destination": destination,"userDetails": userDetails,"context": context, "flag": 0})

            user_id = userDetails['user_id']
            selected_flight_id = request.session.get('selected_flight_id')
            selected_hotel_id = request.session.get('selected_hotel_id')
            selected_destination_id = request.session.get('selected_destination_id')

            destination = DestinationModel.objects.get(Destination_id=selected_destination_id)
            destination_stay = DestinationstayModel.objects.filter(Destination=destination)

            flight = flightClassModel.objects.get(flightClass_id=selected_flight_id)
            hotel = destinationHotelModel.objects.get(destinationHotel_id=selected_hotel_id)

            check_in_date = datetime.strptime(flight.flightDetails.flightDetails_date, '%d/%m/%Y').date()
            check_out_date = datetime.strptime(flight.flightDetails.flightDetails_return_date, '%d/%m/%Y').date()
            
            stay_duration = (check_out_date - check_in_date).days
            stay_duration_night = (stay_duration - 1)
            
            return render(request, 'booking_detail.html', {"stay_duration_night":stay_duration_night,"stay_duration":stay_duration,"destination_stay":destination_stay,"flight": flight, "hotel": hotel, "destination": destination,"userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'booking_detail.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')
    
    
def bookingpaymentFun(request):
    context = {
            "header" : "header header-theme",
            "mainheaderClass" : "",
            "headerClass" : "",
            "listheader" : "list-buttons light",
            "alistheader" : "bg-primary",

        }
    try:
        userDetails = request.session.get("userinfo")
        
        if userDetails:
            if request.method == "POST":
                user_id = userDetails.get("user_id")
                bookingSuccessful_firstname_ = request.POST.get('bookingSuccessfulFirstName')
                bookingSuccessful_lastname_ = request.POST.get('bookingSuccessfulLastName')
                bookingSuccessful_email_ = request.POST.get('bookingSuccessfulEmail')
                bookingSuccessful_total_amount_ = request.POST.get('bookingSuccessfulTotalAmount')
                bookingSuccessful_payment_mode_ = request.POST.get('bookingSuccessfulPaymentMode')
                bookingSuccessful_phoneno_ = request.POST.get('bookingSuccessfulPhoneNo')
                bookingSuccessful_account_number_ = request.POST.get('bookingSuccessfulAccountNumber')
                
                if len(bookingSuccessful_firstname_) <= 0:
                    error ='Please Enter First Name !!'
                    return render(request, 'booking_payment.html', {"error":error, "flag" : 0})
                
                if len(bookingSuccessful_lastname_) <= 0:
                    error ='Please Enter Last Name !!'
                    return render(request, 'booking_payment.html', {"error":error, "flag" : 0})

                if len(bookingSuccessful_email_) <= 0:
                    error ='Please Enter Email !!'
                    return render(request, 'booking_payment.html', {"error":error, "flag" : 0})
                
                
                if len(bookingSuccessful_total_amount_) <= 0:
                    error ='Please Enter Total Amount !!'
                    return render(request, 'booking_payment.html', {"error":error, "flag" : 0})

                if len(bookingSuccessful_phoneno_) <= 0:
                    error ='Please Enter Phone No !!'
                    return render(request, 'booking_payment.html', {"error":error, "flag" : 0})
                
                if not bookingSuccessful_payment_mode_:
                    error ='Please Select Payment No !!'
                    return render(request, 'booking_payment.html', {"error":error, "flag" : 0})
                
                if len(bookingSuccessful_account_number_) <= 0:
                    error ='Please Enter Account Number !!'
                    return render(request, 'booking_payment.html', {"error":error, "flag" : 0})
                
                randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                uniqueID = "User_Guest_" + randomstr

                randomstr = ''.join(random.choices(string.digits, k=6))
                order_invoice_ = randomstr

                user_instance = SignupModel.objects.get(user_id=user_id)

                
                bookingSuccessful = bookingSuccessfulModel(
                    bookingSuccessful_id = uniqueID,
                    user = user_instance,
                    bookingSuccessful_order_invoice = order_invoice_,
                    bookingSuccessful_firstname = bookingSuccessful_firstname_,
                    bookingSuccessful_lastname = bookingSuccessful_lastname_,
                    bookingSuccessful_email = bookingSuccessful_email_,
                    bookingSuccessful_total_amount = bookingSuccessful_total_amount_,
                    bookingSuccessful_payment_mode = bookingSuccessful_payment_mode_,
                    bookingSuccessful_phoneno = bookingSuccessful_phoneno_,
                    bookingSuccessful_account_number = bookingSuccessful_account_number_,

                    
                )
            
                bookingSuccessful.save()

                if bookingSuccessful.bookingSuccessful_id:
                    request.session['booking_successful_data'] = {'user_id': user_id}
                    return redirect(bookingsuccessFun)
                else:
                    return render(request, 'booking_payment.html', {"userDetails": userDetails,"context": context, "flag": 0})
                
            user_id = userDetails['user_id']
            selected_flight_id = request.session.get('selected_flight_id')
            selected_hotel_id = request.session.get('selected_hotel_id')
            selected_destination_id = request.session.get('selected_destination_id')
            current_total_price = request.session.get('total_price')


            destination = DestinationModel.objects.get(Destination_id=selected_destination_id)
            destination_stay = DestinationstayModel.objects.filter(Destination=destination)

            flight = flightClassModel.objects.get(flightClass_id=selected_flight_id)
            hotel = destinationHotelModel.objects.get(destinationHotel_id=selected_hotel_id)
            
                        
            return render(request, 'booking_payment.html', {"current_total_price":current_total_price,"userDetails": userDetails, "context": context, "flag": 1})
        else:
            return render(request, 'booking_payment.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')



def bookingsuccessFun(request):
    context = {
        "header": "header header-theme",
        "mainheaderClass": "",
        "headerClass": "",
        "listheader": "list-buttons light",
        "alistheader": "bg-primary",
    }
    try:
        userDetails = request.session.get("userinfo")
        if userDetails:
            booking_successful_data = request.session.get('booking_successful_data')
            if booking_successful_data:
                booking_successful = bookingSuccessfulModel.objects.filter(user_id=booking_successful_data['user_id']).order_by('-bookingSuccessful_created_at').first()
                if booking_successful:
                    # Clear session after successful payment
                    del request.session['selected_flight_id']
                    del request.session['selected_hotel_id']
                    del request.session['selected_destination_id']

                    return render(request, 'booking_success.html', {"bookingSuccessful": booking_successful, "context": context, "flag": 1})
                else:
                    return render(request, 'booking_success.html', {"context": context, "flag": 0, "error_message": "No booking details found."})
            else:
                return redirect('loginPage')  # Redirect to login page if session data is not present
        else:
            return render(request, 'booking_success.html', {"context": context, "flag": 0})
    except Exception as e:
        print(e)
        return render(request, 'error404.html')
