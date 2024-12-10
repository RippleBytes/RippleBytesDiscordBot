from rest_framework import serializers
from .models import LeaveRequest,TaskRecord,CheckinRecord,BreakRecord



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