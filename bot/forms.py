from django import forms
from .models import LeaveRequest
from django.contrib.auth.models import User
leave_status=(
        ('Requested','Requested'),
        ('Approved','Approved'),
        ('Rejected','Rejected')
    )
class Leaveapprovalform(forms.ModelForm):   
    user_id=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    username=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    leave_type=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    status=forms.ChoiceField(choices=leave_status)
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


class RegistrationForm(forms.ModelForm):
    email=forms.EmailField(max_length=100,label="",widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    first_name=forms.CharField(max_length=100,label="",widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name=forms.CharField(max_length=100,label="",widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    password1=forms.CharField(max_length=100,label="",widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2=forms.CharField(max_length=100,label="",widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Confirm password'}))

    class Meta:
        model=User
        fields=('username','email','first_name','last_name','password1','password2')


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
            
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
    
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'