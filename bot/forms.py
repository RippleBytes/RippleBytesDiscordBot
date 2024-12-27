from django import forms
from .models import LeaveRequest,Employee,BankDetails
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
leave_status=[
        ('Requested','Requested'),
        ('Approved','Approved'),
        ('Rejected','Rejected')
        ]
gender=[
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
]
banks_of_nepal =  [
    ('Agriculture Development Bank Ltd.', 'Agriculture Development Bank Ltd.'),
    ('Bank of Kathmandu Ltd.', 'Bank of Kathmandu Ltd.'),
    ('Century Commercial Bank Ltd.', 'Century Commercial Bank Ltd.'),
    ('Citizens Bank International Ltd.', 'Citizens Bank International Ltd.'),
    ('Civil Bank Ltd.', 'Civil Bank Ltd.'),
    ('Everest Bank Ltd.', 'Everest Bank Ltd.'),
    ('Global IME Bank Ltd.', 'Global IME Bank Ltd.'),
    ('Himalayan Bank Ltd.', 'Himalayan Bank Ltd.'),
    ('Janata Bank Nepal Ltd.', 'Janata Bank Nepal Ltd.'),
    ('Kumari Bank Ltd.', 'Kumari Bank Ltd.'),
    ('Laxmi Bank Ltd.', 'Laxmi Bank Ltd.'),
    ('Machhapuchchhre Bank Ltd.', 'Machhapuchchhre Bank Ltd.'),
    ('Mega Bank Nepal Ltd.', 'Mega Bank Nepal Ltd.'),
    ('Nabil Bank Ltd.', 'Nabil Bank Ltd.'),
    ('Nepal Bangladesh Bank Ltd.', 'Nepal Bangladesh Bank Ltd.'),
    ('Nepal Bank Ltd.', 'Nepal Bank Ltd.'),
    ('Nepal Credit and Commerce Bank Ltd.', 'Nepal Credit and Commerce Bank Ltd.'),
    ('Nepal Investment Bank Ltd.', 'Nepal Investment Bank Ltd.'),
    ('Nepal SBI Bank Ltd.', 'Nepal SBI Bank Ltd.'),
    ('NIC Asia Bank Ltd.', 'NIC Asia Bank Ltd.'),
    ('NMB Bank Ltd.', 'NMB Bank Ltd.'),
    ('Prabhu Bank Ltd.', 'Prabhu Bank Ltd.'),
    ('Prime Commercial Bank Ltd.', 'Prime Commercial Bank Ltd.'),
    ('Rastriya Banijya Bank Ltd.', 'Rastriya Banijya Bank Ltd.'),
    ('Sanima Bank Ltd.', 'Sanima Bank Ltd.'),
    ('Siddhartha Bank Ltd.', 'Siddhartha Bank Ltd.'),
    ('Standard Chartered Bank Nepal Ltd.', 'Standard Chartered Bank Nepal Ltd.'),
    ('Sunrise Bank Ltd.', 'Sunrise Bank Ltd.'),
]


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields='__all__'

class LeaveApprovalForm(forms.ModelForm):   
    user_id=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    username=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    leave_type=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    reason=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    status=forms.ChoiceField(choices=leave_status,widget=forms.widgets.Select(attrs={'class':'form-control'}))
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


class RegistrationForm(UserCreationForm):
    username=forms.CharField(max_length=100,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'abc@abc.com','name':'email'}))
    email=forms.EmailField(max_length=100,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'abc@abc.com','name':'email'}))
    first_name=forms.CharField(max_length=100,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'John','name':'first_name'}))
    last_name=forms.CharField(max_length=100,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Doe','name':'last_name'}))
    discord_user_id=forms.CharField(max_length=18,label="Discord User Id",widget=forms.widgets.TextInput(attrs={'class':'form-control','name':'discord_user_id'}))
    job_title=forms.CharField(max_length=20,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Full-stack developer,Frontend developer,Backend developer','name':'job_title'}))
    phone_number=forms.CharField(max_length=10,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'9841000000','name':'phone_number'}))
    date_of_birth=forms.DateField(label='Date of Birth(A.D.)',widget=forms.widgets.DateInput(attrs={'class':'form-control','type':'date','name':'date_of_birth'}))
    gender=forms.ChoiceField(choices=gender,required=False,widget=forms.widgets.Select(attrs={'class':'form-control','name':'gender'}))
    employee_citizenship_number=forms.CharField(max_length=14,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'**-**-**-*****','name':'employee_citizenship_number'}))
    employee_citizenship_photo=forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':'form-control','placeholder':'.jpg, .jpeg, .png, .gif'}))
    employee_resume_pdf=forms.FileField(required=False,widget=forms.FileInput(attrs={'class':'form-control','placeholder':'.pdf'}))
    employee_pp_photo=forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':'form-control','placeholder':'.jpg, .jpeg, .png, .gif'}))
    class Meta:
        model=User
        fields=('username','email','first_name','last_name','discord_user_id','job_title','phone_number','password1','password2')


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
            
        self.fields['username'].widget.attrs['class'] = 'form-control'
        # self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'Username'
        # self.fields['username'].disabled=True
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
    
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'



class EmployeeBankDetailForm(forms.ModelForm):
    
    bank_name=forms.ChoiceField(choices=banks_of_nepal,widget=forms.widgets.Select(attrs={'class':'form-control','placeholder':'NIC ASIA,GLOBAL IME,....','name':'bank_name'}))
    bank_branch_location=forms.CharField(max_length=100,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Ason,Hattiban,..','name':'bank_branch_location'}))
    employee_bank_account_name=forms.CharField(max_length=100,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Do','name':'employee_bank_account_name'}))
    employee_bank_account_number=forms.CharField(max_length=50,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'00000','name':'employee_bank_account_number'}))
    employee_pan_number=forms.CharField(max_length=15,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'*******','name':'employee_pan_number'}))
    employee_pan_photo=forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':'form-control','name':'employee_pan_photo'}))
    class Meta:
        model=BankDetails
        exclude=('user',)
