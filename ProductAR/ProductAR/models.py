from django.db import models

class userModel(models.Model):
    class Meta:
        db_table = 'user_tb'
    user_id = models.CharField(default=None, max_length=60, primary_key=True)
    user_fname = models.CharField(max_length = 30, default=None, blank=True, null=True)
    user_lname = models.CharField(max_length = 30, default=None, blank=True, null=True)
    user_mobile_num = models.CharField(max_length = 15, default=None, blank=True, null=True)
    user_username = models.CharField(max_length = 100, default=None, blank=True, null=True)
    user_email = models.CharField(max_length = 100, default=None, blank=True, null=True)
    user_password = models.CharField(max_length = 256, default=None, blank=True, null=True)
    user_created_at = models.DateTimeField(auto_now_add=True)
    user_created_at_update = models.CharField(max_length=100, default=None, blank=True, null=True)

class customizeModel(models.Model):
    class Meta:
        db_table = "customizemodel_tb"
    user = models.ForeignKey(userModel, on_delete=models.CASCADE, default=None,blank=True, null=True)
    customize_id = models.CharField(default=None, max_length=60, primary_key=True)
    customize_image = models.TextField(default=None, blank=True, null=True)
    customize_video_path = models.TextField(default=None, blank=True, null=True)
    customize_video_download_link = models.TextField(default=None, blank=True, null=True)
    customize_video_AmbientLight = models.CharField(max_length = 100, default=None, blank=True, null=True)
    customize_video_PointLight = models.CharField(max_length = 100, default=None, blank=True, null=True)
    customize_video_DirectionalLight = models.CharField(max_length = 100, default=None, blank=True, null=True)
    customize_video_SpotLight = models.CharField(max_length = 100, default=None, blank=True, null=True)
    customize_video_Dimension = models.CharField(max_length = 100, default=None, blank=True, null=True)
    customize_created_at = models.DateTimeField(auto_now_add=True)
