from rest_framework import serializers

from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UploadPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
    
class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = notesModel
        fields = "__all__"
        
class FoderfilenameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoderfilenameModel
        fields = "__all__"
        
class FoldernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoldernameModel
        fields = "__all__"
        
class SchedularSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchedularModel
        fields = "__all__"
        
class ExamdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamdetailsModel
        fields = "__all__"