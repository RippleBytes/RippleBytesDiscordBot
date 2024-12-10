from django import forms
from .models import LeaveRequest
leave_status=[
        ('Requested','Requested'),
        ('Approved','Approved'),
        ('Rejected','Rejected')
    ]

class Leaveapprovalform(forms.ModelForm):   
    user_id=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    username=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    leave_type=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    reason=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    
    start_date=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    end_date=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
     
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