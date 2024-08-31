from django.contrib import admin

from .models import *


admin.site.register(Otp)
admin.site.register(AuthToken)
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(CompletedTaskCount)
admin.site.register(SchedularModel)
