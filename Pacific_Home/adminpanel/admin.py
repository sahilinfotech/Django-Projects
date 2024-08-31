from django.contrib import admin
from .models import bangalowModel,visitorModel,clientModel,moneyManagementModel,resumeModel

# Register your models here.

admin.site.register(bangalowModel)
admin.site.register(visitorModel)
admin.site.register(clientModel)
admin.site.register(moneyManagementModel)
admin.site.register(resumeModel)
