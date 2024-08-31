from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.utils.timezone import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
import os
import math
import datetime
import pytz
import random
import string
from django.utils import timezone
from .models import *
from account.models import UserAccount
from .helpers import send_notifying_email
from .serializers import *
from datetime import datetime


def generate_token():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class LoginView(APIView):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = UserAccount.objects.filter(email=email).first()
        user = authenticate(email=email, password=password)

        token = generate_token()

        AuthToken.objects.create(
            user=user_obj,
            token=token
        )
        return Response({"token": token})


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


class RegisterView(APIView):
    def post(self, request):
         
        print("yash pTELLLLL")

        print(request.data)

        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # confirm_password = request.POST.get('confirm_password')

        # {'first_name': 'yash', 'last_name': 'patel', 'email': 'patelyash2504@gmail.com', 'password': 'P@telyash07', 'confirm_password': 'P@telyash07'}
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        password = request.data['password']
        confirm_password = request.data['confirm_password']

        user_obj = UserAccount(email=email, first_name=first_name, last_name=last_name)
        user_obj.set_password(password)
        user_obj.save()

        otp = generate_otp()
        Otp.objects.create(user=user_obj, verifying_otp=otp)

        subject = "Account Activation Required"
        email_template_name = "member/activation.html"
        c = {
            "otp": otp,
        }

        html_content = render_to_string(email_template_name, c)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return Response({"status": "Ok"})


class ActivationView(APIView):
    def post(self, request):
        otp = request.POST.get('otp')
        print(otp)
        try:
            otp_obj = Otp.objects.filter(verifying_otp=otp).first()
            user_obj = UserAccount.objects.get(email=otp_obj.user.email)

            token = generate_token()

            AuthToken.objects.create(
                user=user_obj,
                token=token
            )
            return Response({"token": token})
        except:
            return Response({"status": "fail"})


class RecoverView(APIView):
    def post(self, request):
        email = request.POST.get('email')
        otp = generate_otp()

        user_obj = UserAccount.objects.filter(email=email).first()
        Otp.objects.create(user=user_obj, verifying_otp=otp)

        subject = "Password Reset Requested"
        email_template_name = "member/reset.html"
        c = {
            "otp": otp,
        }
        request.session['otp']=None
        request.session['otp']=otp
        html_content = render_to_string(email_template_name, c)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return Response({"status": "Ok"})


class ResetOtpView(APIView):
    def post(self, request):
        otp = request.POST.get('otp')
        if request.session['otp'] == otp:
            return Response({"status": "Ok"})


class PasswordResetView(APIView):
    def post(self, request):
        password = request.POST.get('password')

        latest_otp = Otp.objects.all().order_by('-id').first()

        user_obj = UserAccount.objects.get(email=latest_otp.user.email)
        user_obj.set_password(password)
        user_obj.save()
        return Response({"status": "Ok"})


class ProfileInfo(APIView):
    def post(self, request):
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        profile, created = Profile.objects.get_or_create(user=user_obj)

        return Response({
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
            "email": user_obj.email,
            "bio": profile.bio,
            "phone": profile.phone,
            "occupation": profile.occupation,
            "hobby": profile.hobby,
            "address": profile.address,
            "country": profile.country,
        })


class ProfileInformation(APIView):
    def post(self, request):
        bio = request.POST.get('bio')
        phone = request.POST.get('phone')
        occupation = request.POST.get('occupation')
        hobby = request.POST.get('hobby')
        address = request.POST.get('address')
        country = request.POST.get('country')
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        profile = Profile.objects.get(user__email=user_obj.email)

        if bio:
            profile.bio = bio
        if phone:
            profile.phone = phone
        if occupation:
            profile.occupation = occupation
        if hobby:
            profile.hobby = hobby
        if address:
            profile.address = address
        if country:
            profile.country = country
        profile.save()


        return Response({"status": "Ok"})


class ProfilePic(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        profile_pic = request.FILES['picture']
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        profile, created = Profile.objects.get_or_create(user__email=auth_token.user.email)
        # fss = FileSystemStorage()
        # file = fss.save(profile_pic.name, profile_pic)
        # file_url = fss.url(file)

        profile.picture = profile_pic
        profile.save()


        return Response({"status": "Ok"})


class EventListView(APIView):
    def post(self, request):
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        events = Event.objects.filter(user__email=user_obj.email).order_by('start')

        data = []
        for event in events:
            start = event.start.astimezone(pytz.timezone('Asia/Dhaka'))
            start = start.strftime('%Y-%m-%d %H:%M:%S.%f')

            end = event.end.astimezone(pytz.timezone('Asia/Dhaka'))
            end = end.strftime('%Y-%m-%d %H:%M:%S.%f')

            data.append(
                {
                    "id": event.id,
                    "title": event.title,
                    "start": start,
                    "end": end,
                    "status": event.status,
                    "location": event.location,
                    "type": event.type,
                    "reminder": event.reminder,
                    "repetition": event.repetition,
                    "description": event.description,
                    "color": event.color,
                }
            )
        # event_serializer = EventSerializer(events)
        return Response(data)


class TodayEventListView(APIView):    
    def post(self, request):
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        raw_events = Event.objects.filter(user__email=user_obj.email).order_by('start')
        today = datetime.datetime.now()
        today_date = today.strftime('%d')

        collected_events = []
        for raw_event in raw_events:
            raw_start = raw_event.start.astimezone(pytz.timezone('Asia/Dhaka'))
            raw_start = raw_start.strftime('%d')

            if raw_start == today_date:
                collected_events.append(raw_event)

        data = []
        for event in collected_events:
            start = event.start.astimezone(pytz.timezone('Asia/Dhaka'))
            start = start.strftime('%Y-%m-%d %H:%M:%S.%f')

            end = event.end.astimezone(pytz.timezone('Asia/Dhaka'))
            end = end.strftime('%Y-%m-%d %H:%M:%S.%f')

            data.append(
                {
                    "id": event.id,
                    "title": event.title,
                    "start": start,
                    "end": end,
                    "status": event.status,
                    "location": event.location,
                    "type": event.type,
                    "reminder": event.reminder,
                    "repetition": event.repetition,
                    "description": event.description,
                    "color": event.color,
                }
            )

        return Response(data)


class EventCalendarView(APIView):    
    def post(self, request):
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        events = Event.objects.filter(user__email=user_obj.email).order_by('start')

        data = {}
        for event in events:
            startDate = event.start.astimezone(pytz.timezone('Asia/Dhaka'))
            startDate = startDate.strftime('%Y-%m-%d')

            start = event.start.astimezone(pytz.timezone('Asia/Dhaka'))
            start = start.strftime('%Y-%m-%d %H:%M:%S.%f')

            end = event.end.astimezone(pytz.timezone('Asia/Dhaka'))
            end = end.strftime('%Y-%m-%d %H:%M:%S.%f')

            data[startDate] = []
            data.update({
                startDate: [
                    {
                        "id": event.id,
                        "title": event.title,
                        "start": start,
                        "end": end
                    }
                ]
            })

        return Response(data)


class EventDayView(APIView):    
    def post(self, request):
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        selected_date_str = request.POST.get('selectedDate')
        # selected_date_obj = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d')   # 2023-10-26 00:00:00   (datetime object)
        # selected_date_obj_tz = selected_date_obj.astimezone(pytz.timezone('Asia/Dhaka'))    # 2023-10-26 00:00:00+06:00   (datetime object with timezone)    

        events = Event.objects.filter(user__email=user_obj.email)

        dayEvents = []
        for event in events:
            start = event.start.astimezone(pytz.timezone('Asia/Dhaka'))
            end = event.end.astimezone(pytz.timezone('Asia/Dhaka'))

            startDate = start.strftime('%Y-%m-%d')

            if startDate == selected_date_str:
                day_event = {
                    "id": event.id,
                    "title": event.title,
                    'startHour': start.strftime('%H'),
                    'start': start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    'end': end.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    'color': event.color
                }
                dayEvents.append(day_event)

        return Response(dayEvents)


class EventDetailView(APIView):    
    def post(self, request):
        id = int(request.POST.get('id'))
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        event = Event.objects.get(id=id, user__email=user_obj.email)

        start = event.start.astimezone(pytz.timezone('Asia/Dhaka'))
        start = start.strftime('%Y-%m-%d %H:%M:%S.%f')

        end = event.end.astimezone(pytz.timezone('Asia/Dhaka'))
        end = end.strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {
            "id": event.id,
            "title": event.title,
            "start": start,
            "end": end,
            "location": event.location,
            "type": event.type,
            "reminder": event.reminder,
            "repetition": event.repetition,
            "description": event.description
        }
        # event_serializer = EventSerializer(event)
        return Response(data)


class AddEventView(APIView):    
    def post(self, request):
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')
        location = request.POST.get('location')
        type = request.POST.get('type')
        reminder = request.POST.get('reminder')
        repetition = request.POST.get('repetition')
        color = request.POST.get('color')
        description = request.POST.get('description')
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        stripped_start = start.strip()
        if 'Z' in stripped_start:
            start = start.strip('Z')

        stripped_end = end.strip()
        if 'Z' in stripped_end:
            end = end.strip('Z')

        start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        start = start.astimezone(pytz.timezone('Asia/Dhaka'))

        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        end = end.astimezone(pytz.timezone('Asia/Dhaka'))

        user = UserAccount.objects.get(email=user_obj.email)

        Event.objects.create(
            user=user,
            title=title,
            start=start,
            end=end,
            location=location,
            type=type,
            reminder=reminder,
            repetition=repetition,
            color=color,
            description=description
        )

        return Response({"status": "saved"})


class EditEventView(APIView):    
    def post(self, request):
        id = int(request.POST.get('id'))
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')
        location = request.POST.get('location')
        type = request.POST.get('type')
        reminder = request.POST.get('reminder')
        repetition = request.POST.get('repetition')
        description = request.POST.get('description')
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        start = start.astimezone(pytz.timezone('Asia/Dhaka'))

        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        # end = end.astimezone(pytz.utc)
        end = end.astimezone(pytz.timezone('Asia/Dhaka'))

        event = Event.objects.get(id=id, user__email=user_obj.email)

        if title:
            event.title = title
        if start:
            event.start = start
        if end:
            event.end = end
        if location:
            event.location = location
        if type:
            event.type = type
        if reminder:
            event.reminder = reminder
        if repetition:
            event.repetition = repetition
        if description:
            event.description = description
        event.save()

        
        return Response({"status": "edited"})


class MarkEventView(APIView):    
    def post(self, request):
        id = int(request.POST.get('id'))
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        event = Event.objects.get(id=id, user__email=user_obj.email)
        event.status = "Completed"
        event.save()

        pallete, created = CompletedTaskCount.objects.get_or_create(user=user_obj)

        if created:
            pallete.numberOfTasks = 1
            pallete.save()
        else:
            pallete.numberOfTasks += 1
            pallete.save()

        return Response({"status": "Ok"})
    

class CompletedTasksCountView(APIView):    
    def post(self, request):
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        pallete, created = CompletedTaskCount.objects.get_or_create(user=user_obj)

        if created:
            number = 0
        else:
            number = pallete.numberOfTasks

        return Response({"number": number})
    

class DeleleEventView(APIView):    
    def post(self, request):
        id = int(request.POST.get('id'))
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        event = Event.objects.get(id=id, user__email=user_obj.email)
        event.delete()

        
        return Response({"status": "deleted"})
    

def notify_user():
    events = Event.objects.filter().order_by('start')
    
    if len(events) > 0:
        for event in events:
            time_diff = event.start - timezone.now()
            if time_diff.total_seconds() >= -60 and time_diff.total_seconds() <= 60:
                send_notifying_email(event)
                
                Notification.objects.create(
                    title = event.title,
                    desc = event.description,
                    start = event.start,
                )
                
                event.notified = True
                event.save()
                break 


class NotificationsView(APIView):
    def post(self, request):
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        notifications = Notification.objects.filter(user__email=user_obj.email).order_by('-start')

        data = []
        if len(notifications) > 0:
            for notification in notifications:
                data.append({
                    "id": notification.id,
                    "title": notification.title,
                    "desc": notification.desc,
                    "start": notification.start
                })
        
        return Response(data)

class PushNotificationView(APIView):    
    def post(self, request):
        token = request.POST.get('token')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        # Retrieve all notifications associated with the user_id
        # notifications = PushNotification.objects.filter(user_id=user_obj)
        notifications = PushNotification.objects.filter(user=user_obj).order_by('-created_at')
        data = []
        if notifications:
            for notification in notifications:
                data.append({
                    "message": notification.message,
                    "created_at": notification.created_at
                })
        
        return Response(data)

class AddPushNotificationView(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        message = request.POST.get('message')
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        
        inqinfo = PushNotification(user=user_obj, message=message)
        inqinfo.save()
        
        return Response({"status": "Ok"})
    

class AddNotesFun(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        notesname = request.POST.get('notesname')
        notesdescription = request.POST.get('notesdescription')
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        print(user_obj,'aaaaa')
        inqinfo = notesModel(user=user_obj, notesname=notesname,notesdescription=notesdescription)
        inqinfo.save()
        
        return Response({"status": "Ok"})
    
class UpdateNotesFun(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        notesname = request.POST.get('notesname')
        notesdescription = request.POST.get('notesdescription')
        id = request.POST.get('id')
        
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        
        UPDATEDATA=notesModel.objects.get(pk=id)
        UPDATEDATA.notesname = notesname
        UPDATEDATA.notesdescription = notesdescription
        UPDATEDATA.save()
        return Response({"status": "Ok"})
    
class getNotesFun(APIView):    
    def post(self, request):
        token = request.POST.get('token')
        print(token,'ooooooooooooooooooo')
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        print('ssyash',user_obj)
        # notes = notesModel.objects.values()

        notes = notesModel.objects.filter(user=user_obj).values().order_by('-created_at')
        print(notes,'ssssscccccccccccccccccccccccccccc')
        # data = []
        # if notes:
        #     for note in notes:
        #         data.append({
        #             "notesname": note.notesname,
        #             "notesdescription": note.notesdescription,
        #             "user":note.user,
        #             "created_at": note.created_at
        #         })
        
        return Response(notes)

class getNotesUsingIDFun(APIView):    
    def post(self, request):
        id = request.POST.get('id')

        # auth_token = AuthToken.objects.filter(token=token).first()
        # user_obj = UserAccount.objects.get(email=auth_token.user.email)

        notes = notesModel.objects.filter(pk=id).order_by('-created_at')
        data = []
        if notes:
            for note in notes:
                data.append({
                    "notesname": note.notesname,
                    "notesdescription": note.notesdescription,
                    "user":note.user,
                    "created_at": note.created_at
                })
        
        return Response(data)

class DeleteNotesFun(APIView):    
    def post(self, request):
        id = request.POST.get('id')

        # for i in id:
        print(id[0])
        notes = notesModel.objects.get(pk=int(id))
        notes.delete()
        return Response({"status": "deleted"})

class DeleteUserFun(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        
        user_obj.delete()
        
        return Response({"status": "deleted"})
    
    
class AddfoldernameFun(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        foldername = request.POST.get('foldername')
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        
        inqinfo = FoldernameModel(user=user_obj, foldername=foldername)
        inqinfo.save()
        
        return Response({"status": "Ok"})
    

    
class UpdatefoldernameFun(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        foldername = request.POST.get('foldername')
        # notesdescription = request.POST.get('notesdescription')
        id = request.POST.get('id')
        
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        
        UPDATEDATA=FoldernameModel.objects.get(pk=id)
        UPDATEDATA.foldername = foldername
        UPDATEDATA.save()
        return Response({"status": "Ok"})
    
class getfoldernameFun(APIView):    
    def post(self, request):
        token = request.POST.get('token')
        print(token,'ssssss')
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)

        # notes = FoldernameModel.objects.values()
        print('ssssssssssssss',user_obj)

        notes = FoldernameModel.objects.filter(user_id=user_obj).values().order_by('-created_at')
        print(notes)
        # data = []
        # if notes:
        #     for note in notes:
        #         data.append({
        #             "foldername": note.foldername,
        #             "user":note.user,
        #             "created_at": note.created_at
        #         })
        
        return Response(notes)

class getfoldernameUsingIDFun(APIView):    
    def post(self, request):
        id = request.POST.get('id')

        # auth_token = AuthToken.objects.filter(token=token).first()
        # user_obj = UserAccount.objects.get(email=auth_token.user.email)

        notes = FoldernameModel.objects.filter(pk=id).order_by('-created_at')
        data = []
        if notes:
            for note in notes:
                data.append({
                    "foldername": note.foldername,
                    "user":note.user,
                    "created_at": note.created_at
                })
        
        return Response(data)

class DeletefoldernameFun(APIView):    
    def post(self, request):
        id = request.POST.get('id')

        # for i in id:
        print(id[0])
        notes = FoldernameModel.objects.get(pk=int(id))
        notes.delete()
        return Response({"status": "deleted"})



class AddfolderfilenameFun(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        foldername = request.POST.get('foldername')
        folderfile = request.FILES.get('folderfile')
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        
        department_instance = FoldernameModel.objects.get(pk=foldername)
        
        inqinfo = FoderfilenameModel(user=user_obj, foldername=department_instance,folderfile=folderfile)
        inqinfo.save()
        
        return Response({"status": "Ok"})
    
class UpdatefolderfilenameFun(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        foldername = request.POST.get('foldername')
        folderfile = request.FILES.get('folderfile')
        id = request.POST.get('id')
        
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        department_instance = FoldernameModel.objects.get(pk=foldername)

        UPDATEDATA=FoderfilenameModel.objects.get(pk=id)
        UPDATEDATA.folderfile.delete()
        UPDATEDATA.foldername = department_instance
        UPDATEDATA.folderfile = folderfile
        UPDATEDATA.save()
        return Response({"status": "Ok"})
    
# class getfolderfilenameFun(APIView):    
#     def post(self, request):
#         token = request.POST.get('token')

#         auth_token = AuthToken.objects.filter(token=token).first()
#         user_obj = UserAccount.objects.get(email=auth_token.user.email)

#         notes = FoldernameModel.objects.filter(user=user_obj).order_by('-created_at')
#         data = []
#         if notes:
#             for note in notes:
#                 data.append({
#                     "foldername": note.foldername,
#                     "user":note.user,
#                     "created_at": note.created_at
#                 })
        
#         return Response(data)

class getfolderfilenameUsingIDFun(APIView):    
    def post(self, request):
        print(request.POST,'sss')
        id = request.POST.get('id')

        # auth_token = AuthToken.objects.filter(token=token).first()
        # user_obj = UserAccount.objects.get(email=auth_token.user.email)
        print(id,'pplplpl')
        notes = FoderfilenameModel.objects.filter(foldername_id=id).values().order_by('-created_at')
        print(notes)
        # data = []
        
        
        return Response(notes)

class DeletefolderfilenameFun(APIView):    
    def post(self, request):
        id = request.POST.get('id')

        # for i in id:
        print(id,'ddddddddddddddddddddddddddd')
        notes = FoderfilenameModel.objects.get(pk=int(id))
        notes.delete()
        return Response({"status": "deleted"})
    
    
###############################################
class AddSchedularFun(APIView):    
    def post(self, request):
        print(request.POST,'ssssssssssssssssssssssssss')
        token = request.POST.get('token')
        remindertime = request.POST.get('remindertime')
        color = request.POST.get('color')
        endtime = request.POST.get('endtime')
        starttime = request.POST.get('starttime')
        subjectname = request.POST.get('subjectname')
        description = request.POST.get('description')
        isExam = request.POST.get('isExam')
        isschedular = request.POST.get('isschedular')
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        
        print(datetime.fromisoformat(request.POST.get('starttime')),'starttime')
        print(datetime.fromisoformat(request.POST.get('endtime')),'endtime')
        overlapping_events = SchedularModel.objects.filter(
            user=user_obj,
            starttime__lt=endtime,
            endtime__gt=starttime,
        ).exists()
        
        if overlapping_events:
            return Response({"status": "Time slot is already taken"})
       
        
        # if SchedularModel.objects.filter(starttime = starttime,endtime=endtime,user=user_obj).exists():
        
        #     return Response({"status": "Time is already schedule"})
        else:
        
        # inqinfo = SchedularModel(user=user_obj, remindertime=remindertime,color=color,endtime=endtime,subjectname=subjectname,starttime=starttime)
        # inqinfo.save()
            inqinfo = SchedularModel(
                user=user_obj,
                remindertime=remindertime,
                color=color,
                endtime=endtime,
                subjectname=subjectname,
                starttime=starttime,
                isExam=isExam,
                isschedular=isschedular
            )
            inqinfo.save()
            
            serialized_data = SchedularSerializer(inqinfo).data
            
            return Response({"status": "Ok", "data": serialized_data})
        
        
        # inqinfo = SchedularModel(user=user_obj, remindertime=remindertime,color=color,endtime=endtime,subjectname=subjectname,starttime=starttime)
        # inqinfo.save()
        # inqinfo = SchedularModel(
        #     user=user_obj,
        #     remindertime=remindertime,
        #     color=color,
        #     endtime=endtime,
        #     subjectname=subjectname,
        #     starttime=starttime,
        #     isExam=isExam,
        #     isschedular=isschedular
        # )
        # inqinfo.save()
        
        # serialized_data = SchedularSerializer(inqinfo).data
        
        # return Response({"status": "Ok", "data": serialized_data})

    
class DeleteSchedularFun(APIView):    
    def post(self, request):
        id = request.POST.get('id')

        # for i in id:
        print(id,'ddddddddddddddddddddddddddd')
        notes = SchedularModel.objects.get(pk=int(id))
        notes.delete()
        return Response({"status": "deleted"})
    

class getSchedularallFun(APIView):    
    def post(self, request):
        print(request.POST,'sss')
        token = request.POST.get('token')
        print(token)
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        print(user_obj,'pplplpl')
        notes = SchedularModel.objects.filter(user_id=user_obj).values().order_by('-created_at')
        print(notes)
    
        return Response(notes)
    
class UpdateSchedularFun(APIView):    
    def post(self, request):

        # token = request.POST.get('token')
        remindertime = request.POST.get('remindertime')
        color = request.POST.get('color')
        endtime = request.POST.get('endtime')
        starttime = request.POST.get('starttime')
        subjectname = request.POST.get('subjectname')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed')
        isExam = request.POST.get('isExam')
        isschedular = request.POST.get('isschedular')
        id = request.POST.get('id')
        
        
        # auth_token = AuthToken.objects.filter(token=token).first()
        # user_obj = UserAccount.objects.get(email=auth_token.user.email)

        UPDATEDATA=SchedularModel.objects.get(pk=id)
        UPDATEDATA.color = color
        UPDATEDATA.remindertime = remindertime
        UPDATEDATA.endtime = endtime
        UPDATEDATA.starttime = starttime
        UPDATEDATA.description = description
        UPDATEDATA.subjectname = subjectname
        UPDATEDATA.is_completed = is_completed
        UPDATEDATA.isExam = isExam
        UPDATEDATA.isschedular = isschedular
        UPDATEDATA.save()
        return Response({"status": "Ok"})
    

# class getSchedularTodayFun(APIView):    
#     def post(self, request):
#         token = request.POST.get('token')
#         today = timezone.now().date()
#         print(today,'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
#         auth_token = AuthToken.objects.filter(token=token).first()
#         user_obj = UserAccount.objects.get(email=auth_token.user.email)
#         print(user_obj,'pplplpl')
#         notes = SchedularModel.objects.filter(
#             user_id=user_obj,
#             starttime=today
#         ).values().order_by('-created_at')
#         print(notes)
    
#         return Response(notes)


class getSchedularTodayFun(APIView):    
    def post(self, request):
        token = request.POST.get('token')
        today = timezone.now().date()
        print(today,'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        print(user_obj,'pplplpl')
        
        # Filter the SchedularModel based on the user and today's date range
        notes = SchedularModel.objects.filter(
            user_id=user_obj
        ).values().order_by('-created_at')
        
        print(notes)
        return Response(notes)
    
    

#############################################################################################
###############################################
class AddexamdetailsFun(APIView):    
    def post(self, request):

        token = request.POST.get('token')
        remindertime = request.POST.get('remindertime')
        color = request.POST.get('color')
        endtime = request.POST.get('endtime')
        starttime = request.POST.get('starttime')
        subjectname = request.POST.get('subjectname')
        
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        
        
        # inqinfo = SchedularModel(user=user_obj, remindertime=remindertime,color=color,endtime=endtime,subjectname=subjectname,starttime=starttime)
        # inqinfo.save()
        inqinfo = ExamdetailsModel(
            user=user_obj,
            remindertime=remindertime,
            color=color,
            endtime=endtime,
            subjectname=subjectname,
            starttime=starttime
        )
        inqinfo.save()
        
        serialized_data = ExamdetailsSerializer(inqinfo).data
        
        return Response({"status": "Ok", "data": serialized_data})

    
class DeleteexamdetailsFun(APIView):    
    def post(self, request):
        id = request.POST.get('id')

        # for i in id:
        print(id,'ddddddddddddddddddddddddddd')
        notes = ExamdetailsModel.objects.get(pk=int(id))
        notes.delete()
        return Response({"status": "deleted"})
    

class getexamdetailsallFun(APIView):    
    def post(self, request):
        print(request.POST,'sss')
        token = request.POST.get('token')
        print(token)
        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        print(user_obj,'pplplpl')
        notes = ExamdetailsModel.objects.filter(user_id=user_obj).values().order_by('-created_at')
        print(notes)
    
        return Response(notes)
    
class UpdateexamdetailsFun(APIView):    
    def post(self, request):

        # token = request.POST.get('token')
        remindertime = request.POST.get('remindertime')
        color = request.POST.get('color')
        endtime = request.POST.get('endtime')
        starttime = request.POST.get('starttime')
        subjectname = request.POST.get('subjectname')
        is_completed = request.POST.get('is_completed')
        id = request.POST.get('id')
        
        
        # auth_token = AuthToken.objects.filter(token=token).first()
        # user_obj = UserAccount.objects.get(email=auth_token.user.email)

        UPDATEDATA=ExamdetailsModel.objects.get(pk=id)
        UPDATEDATA.color = color
        UPDATEDATA.remindertime = remindertime
        UPDATEDATA.endtime = endtime
        UPDATEDATA.starttime = starttime
        UPDATEDATA.subjectname = subjectname
        UPDATEDATA.is_completed = is_completed
        UPDATEDATA.save()
        return Response({"status": "Ok"})
    

# class getSchedularTodayFun(APIView):    
#     def post(self, request):
#         token = request.POST.get('token')
#         today = timezone.now().date()
#         print(today,'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
#         auth_token = AuthToken.objects.filter(token=token).first()
#         user_obj = UserAccount.objects.get(email=auth_token.user.email)
#         print(user_obj,'pplplpl')
#         notes = SchedularModel.objects.filter(
#             user_id=user_obj,
#             starttime=today
#         ).values().order_by('-created_at')
#         print(notes)
    
#         return Response(notes)

class getexamdetailsTodayFun(APIView):    
    def post(self, request):
        token = request.POST.get('token')
        today = timezone.now().date()
        print(today,'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

        auth_token = AuthToken.objects.filter(token=token).first()
        user_obj = UserAccount.objects.get(email=auth_token.user.email)
        print(user_obj,'pplplpl')
        
        # Filter the SchedularModel based on the user and today's date range
        notes = ExamdetailsModel.objects.filter(
            user_id=user_obj
        ).values().order_by('-created_at')
        
        print(notes)
        return Response(notes)