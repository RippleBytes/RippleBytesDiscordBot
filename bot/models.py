from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# class Employee(models.Model):
#     user_id=models.CharField(max_length=100)
#     username=models.CharField(max_length=100)
#     full_name=models.CharField(max_length=200)
#     email=models.EmailField(unique=True,null=False,blank=False)
#     phone_number=models.PositiveBigIntegerField(null=False,blank=False)

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

    user_id=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    leave_type=models.CharField(null=False,blank=False,choices=type,default='Annual Leave')
    status=models.CharField(choices=leave_status,null=True,blank=True,default='Requested')
    reason=models.TextField(null=False,blank=False)
    start_date=models.DateField(null=False,blank=False)
    end_date=models.DateField(null=False,blank=False)
    
    

    def __str__(self):
        return f'Leave request for {self.reason}' #{self.user_name},
    
