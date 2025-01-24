from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils.timezone import now
from .validators import validate_image,validate_pdf



gender=[
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
]
type=[
        ( 'Unpaid Leave','Unpaid Leave'),
        ( 'Annual Leave','Annual Leave',),
        ( 'Sick Leave','Sick Leave',),
        ('Unknown','Unknown')     
    ]
leave_status=[
        ('Requested','Requested'),
        ('Approved','Approved'),
        ('Rejected','Rejected')
    ]

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    discord_user_id=models.CharField(blank=False,null=False,unique=True,default=11)
    job_title=models.CharField(max_length=200,blank=False,null=False,default='employee')
    phone_number=models.CharField(max_length=10,blank=False,unique=True,null=False,default=000000)
    date_of_birth=models.CharField(blank=False,null=False,default='2025/10/10')
    gender=models.CharField(choices=gender,blank=False,null=False,default='00')

    private_email=models.EmailField(blank=False,null=False,unique=True,default='abc@gmail.com')

    employee_citizenship_number=models.CharField(blank=False,null=False,max_length=14,default=000000)
    employee_citizenship_photo=models.ImageField(upload_to='EmployeeCitizenship/',blank=True,null=True,default='superuser.jpg')
    employee_resume_pdf=models.FileField(upload_to='EmployeeResume/',blank=True,null=True,default='superuser.pdf')
    employee_pp_photo=models.ImageField(upload_to='EmployeePhoto/',blank=True,null=True,default='superuser.jpg')

    groups = models.ManyToManyField(
        Group,
        related_name='bot_user_groups',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='bot_user_permissions',  
        blank=True,
    )


    def clean(self):
        validate_pdf(self.employee_resume_pdf)
        validate_image(self.employee_citizenship_photo)
        validate_image(self.employee_pp_photo)

    def save(self,*args, **kwargs):
        self.clean()
        super(User,self).save(*args,**kwargs)

    
    def __str__(self):
        return (f"{self.first_name}[{self.id}]({self.discord_user_id})")




class CheckinRecord(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    checkin_time = models.DateTimeField(default=now)
    checkout_time = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.username}({self.user})"

class TaskRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkin=models.ForeignKey(CheckinRecord, related_name='tasks',on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    show=models.BooleanField(default=True)

    def __str__(self):
        return f"Task: {self.task} - Completed: {self.completed}"

class BreakRecord(models.Model):
    checkin = models.ForeignKey(CheckinRecord, related_name='breaks', on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()

    def __str__(self):
        return f"Break for {self.reason} from {self.start_time} to {self.end_time}"



class LeaveRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    leave_type=models.CharField(null=False,blank=False,choices=type,default='Annual Leave')
    status=models.CharField(choices=leave_status,blank=True,null=True,default='Requested')
    reason=models.TextField(null=False,blank=False)
    start_date=models.DateField(null=False,blank=False)
    end_date=models.DateField(null=False,blank=False)
    
    

    def __str__(self):
        return f'{self.username},Reason:{self.reason}'
    


class BankDetail(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bank_name=models.CharField(max_length=100,blank=False,null=False,default='00')
    bank_branch_location=models.CharField(max_length=50,blank=False,null=False,default='Kathmandu')
    employee_bank_account_name=models.CharField(max_length=100,blank=False,null=False,default=00)
    employee_bank_account_number=models.CharField(max_length=50,blank=False,null=False,default=00)
    employee_pan_number=models.PositiveBigIntegerField(blank=False,null=False,default=000)
    employee_pan_photo=models.ImageField(upload_to='EmployeePanCard/',blank=True,null=True,default=None)   

    def clean(self):
        validate_image(self.employee_pan_photo)

    def save(self,*args, **kwargs):
        self.clean()
        super(BankDetail,self).save(*args,**kwargs)

class LateArrival(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reason=models.CharField(max_length=100)
    time_duration=models.CharField(max_length=100)

    def __str__(self):
        return f" Reason:{self.reason}, time:{self.reason} ,user_id:{self.user_id} "