from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from userApp.models import *


def mailSend(request, myuser, randomstr):
    
    try:

        user = SignupModel.objects.get(user_email=myuser)
        email_subject = "Verify your Email @ Dream Trips Login!!"
        message2 = render_to_string('email_confirmation.html',{
            'code': randomstr
        })

        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [user.user_email],
        )
        print(email)
        email.fail_silently = True
        email.send()
        return True
        
    except:

        pass
        
        #raise serializers.ValidationError({"user_email_send":"Email send error"})
