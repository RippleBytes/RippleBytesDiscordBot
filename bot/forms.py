from django import forms
from .models import LeaveRequest


class Leaveapprovalform(forms.ModelForm):    
    class Meta:
        model=LeaveRequest
        fields='__all__'
                
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['user_id'].disabled=True
        self.fields['username'].disabled=True
        self.fields['leave_type'].disabled=True
        self.fields['reason'].disabled=True
        self.fields['start_date'].disabled=True
        self.fields['end_date'].disabled=True