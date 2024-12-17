from rest_framework import serializers
from .models import LeaveRequest,TaskRecord,CheckinRecord,BreakRecord,Employee
from django.contrib.auth.models import User



class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveRequest
        fields='__all__'
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskRecord
        fields='__all__'

class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model=CheckinRecord
        fields='__all__'

class BreakSerializer(serializers.ModelSerializer):
    class Meta:
        model=BreakRecord
        fields='__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        exclude=('id',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','date_joined','first_name','last_name','username','email',]