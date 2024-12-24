from django.db import models
from django.contrib.auth.models import User
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
class Employee(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    discord_user_id=models.CharField(blank=False,null=False,unique=True,default=11)
    job_title=models.CharField(max_length=200,blank=False,null=False,default='employee')
    phone_number=models.PositiveBigIntegerField(blank=False,null=False,default=201231)
    date_of_birth=models.CharField(blank=False,null=False,default='2025/10/10')
    gender=models.CharField(choices=gender,blank=False,null=False,default='00')
    
    employee_citizenship_number=models.CharField(blank=False,null=False,max_length=15,default=000000)
    employee_citizenship_photo=models.ImageField(upload_to='EmployeeCitizenship/',blank=True,null=True)
    employee_resume_pdf=models.FileField(upload_to='EmployeeResume/',blank=True,null=True)
    employee_pp_photo=models.ImageField(upload_to='EmployeePhoto/',blank=True,null=True)


    # def clean(self):
    #     validate_pdf(self.employee_resume_pdf)
    #     validate_image(self.employee_citizenship_photo)
    #     validate_image(self.employee_pan_photo)
    #     validate_image(self.employee_pp_photo)

    def save(self,*args, **kwargs):
        self.clean()
        super(Employee,self).save(*args,**kwargs)
    
    def __str__(self):
        return (f"user:{self.user} discord_user_id{self.discord_user_id}")
class CheckinRecord(models.Model):
    user_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    checkin_time = models.DateTimeField(default=now)
    checkout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.user_id})"

class TaskRecord(models.Model):
    checkin = models.ForeignKey(CheckinRecord, related_name='tasks', on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)

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
    user_id=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    leave_type=models.CharField(null=False,blank=False,choices=type,default='Annual Leave')
    status=models.CharField(choices=leave_status,blank=True,null=True,default='Requested')
    reason=models.TextField(null=False,blank=False)
    start_date=models.DateField(null=False,blank=False)
    end_date=models.DateField(null=False,blank=False)
    
    

    def __str__(self):
        return f'Leave request for {self.reason}' #{self.user_name},
    


class BankDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bank_name=models.CharField(max_length=100,blank=False,null=False,default='00')
    bank_branch_location=models.CharField(max_length=50,blank=False,null=False,default='Kathmandu')
    employee_bank_account_name=models.CharField(max_length=100,blank=False,null=False,default=00)
    employee_bank_account_number=models.CharField(max_length=50,blank=False,null=False,default=00)
    employee_pan_number=models.PositiveBigIntegerField(blank=False,null=False,default=000)
    employee_pan_photo=models.ImageField(upload_to='EmployeePanCard/',blank=False,null=False,default=None)    