from django.db import models

# Bangalow Model
class bangalowModel(models.Model):
    class Meta:
        db_table = "bangalowmodel_tb"
    bangalow_id = models.CharField(max_length=60, primary_key=True,default="None")
    bangalow_no = models.CharField(max_length=100, default="None", blank=True, null=True)
    bangalow_bHK = models.CharField(max_length=100, default="None", blank=True, null=True)
    bangalow_area = models.CharField(max_length=100, default="None", blank=True, null=True)
    bangalow_price = models.CharField(max_length=100, default="None", blank=True, null=True)
    bangalow_is_active = models.CharField(default="None")
    bangalow_created_at = models.DateTimeField(auto_now_add=True)
    bangalow_created_at_update = models.CharField(max_length=100, default="None", blank=True, null=True)

class visitorModel(models.Model):
    class Meta:
        db_table = "visitormodel_tb"
    visitor_id = models.CharField(max_length=60, primary_key=True, default="None")
    bangalow = models.ForeignKey(bangalowModel, on_delete=models.CASCADE, default="None")
    visitor_first_name = models.CharField(max_length=100, default="None", blank=True, null=True)
    visitor_last_name = models.CharField(max_length=100, default="None", blank=True, null=True)
    visitor_location = models.CharField(max_length=100, default="None", blank=True, null=True)
    visitor_email_id = models.CharField(max_length=100, default="None", blank=True, null=True)
    visitor_whatapp_phoneNo = models.CharField(max_length=100, default="None", blank=True, null=True)
    visitor_phoneNo = models.CharField(max_length=100, default="None", blank=True, null=True)
    visitor_is_active = models.CharField(default="None")
    visitor_created_at = models.DateTimeField(auto_now_add=True)
    visitor_created_at_update = models.CharField(max_length=100, default="None", blank=True, null=True)
    
class clientModel(models.Model):
    class Meta:
        db_table = "clientmodel_tb"
    client_id = models.CharField(max_length=60, primary_key=True, default="None")
    visitor = models.ForeignKey(visitorModel, on_delete=models.CASCADE, default="None")
    client_bangalow_no = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_phone_no = models.CharField(max_length=100, default="None", blank=True, null=True) 
    client_first_name = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_last_name = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_email_id = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_aadhar_card_no = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_pan_card_no = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_proof = models.TextField(default="None", blank=True, null=True)
    client_total_price = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_amount_mode = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_transition = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_token_payment = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_total_remaining_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_time_period = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_monthly_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_date = models.CharField(max_length=100, default="None", blank=True, null=True)
    client_is_active = models.CharField(default="None")
    client_created_at = models.DateTimeField(auto_now_add=True)
    client_created_at_update = models.CharField(max_length=100, default="None", blank=True, null=True)
    
    
# class installmentModel(models.Model):
#     class Meta:
#         db_table = "installmentmodel_tb"
#     installment_id = models.CharField(max_length=60, primary_key=True, default="None")
#     client = models.ForeignKey(clientModel, on_delete=models.CASCADE, default="None")
#     installment_bangalow_no = models.TextField(default="None", blank=True, null=True)
#     installment_phone_no = models.CharField(max_length=100, default="None", blank=True, null=True)
#     installment_total_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
#     installment_token_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
#     installment_total_remaining_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
#     installment_amount_mode = models.CharField(max_length=100, default="None", blank=True, null=True)
#     installment_transition = models.CharField(max_length=100, default="None", blank=True, null=True)
#     installment_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
#     installment_remaining_Payment = models.CharField(max_length=100, default="None", blank=True, null=True)
#     installment_date = models.TextField(default="None", blank=True, null=True)
#     installment_is_active = models.CharField(default="None")
#     installment_created_at = models.DateTimeField(auto_now_add=True)
#     installment_created_at_update = models.CharField(max_length=100, default="None", blank=True, null=True)



class moneyManagementModel(models.Model):
    class Meta:
        db_table = "moneymanagementmodel_tb"
    moneyManagement_id = models.CharField(max_length=60, primary_key=True, default="None")
    # visitor = models.ForeignKey(visitorModel, on_delete=models.CASCADE, default="None")
    client = models.ForeignKey(clientModel, on_delete=models.CASCADE, default="None")
    moneyManagement_bangalow_no = models.TextField(default="None", blank=True, null=True)
    moneyManagement_phone_no = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_total_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_token_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_total_remaining_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_amount_mode = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_transition = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_installment_amount = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_remaining_Payment = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_date = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_transition_proof = models.TextField(default="None", blank=True, null=True)
    moneyManagement_cheque_photo = models.TextField(default="None", blank=True, null=True)
    moneyManagement_bank_name = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_bank_branch = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_IFSE_No = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_cheque_No = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_Account_No = models.CharField(max_length=100, default="None", blank=True, null=True)
    moneyManagement_is_active = models.CharField(default="None")
    moneyManagement_created_at = models.DateTimeField(auto_now_add=True)
    moneyManagement_created_at_update = models.CharField(max_length=100, default="None", blank=True, null=True)



class resumeModel(models.Model):
    class Meta:
        db_table = "resumemodel_tb"
    resume_id = models.CharField(max_length=60, primary_key=True, default="None")
    resume_full_name = models.TextField(default="None", blank=True, null=True)
    resume_phone_no = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_email = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_headline = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_address = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_city = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_education = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_school = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_date = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_description = models.TextField(default="None", blank=True, null=True)
    resume_image = models.TextField(default="None", blank=True, null=True)
    resume_project_image = models.TextField(default="None", blank=True, null=True)
    resume_technical_skills = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_soft_skills = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_language = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_hobby = models.CharField(max_length=100, default="None", blank=True, null=True)
    resume_is_active = models.CharField(default="None")
    resume_created_at = models.DateTimeField(auto_now_add=True)
    resume_created_at_update = models.CharField(max_length=100, default="None", blank=True, null=True)
