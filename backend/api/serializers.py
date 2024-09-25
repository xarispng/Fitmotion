from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    
class SessionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Session
        fields = '__all__'

class AdminSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Session
        fields = '__all__'

class FixedSessionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = FixedSession
        fields = '__all__'

class DisabledDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabledDate
        fields = '__all__'

class ReschedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reschedules
        fields = '__all__'