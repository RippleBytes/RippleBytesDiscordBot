from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CheckinRecord,TaskRecord,BreakRecord,LeaveRequest,Employee,BankDetails
class TaskRecordInline(admin.TabularInline):
    model=TaskRecord
    fields=['task','completed']
    readonly_fields=('task','completed',)

@admin.register(CheckinRecord)
class CheckinRecordAdmin(admin.ModelAdmin):
    list_display = ('username', 'checkin_time', 'checkout_time')
    inlines=[TaskRecordInline]

@admin.register(TaskRecord)
class TaskRecordAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'task', 'completed')

@admin.register(BreakRecord)
class BreakRecordAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'start_time', 'end_time', 'reason')
# @admin.register(User)
# class EmployeeAdmin(UserAdmin):
#     model=User
#     fieldsets=(None,{'fields':('user_id','user_name','full_name','phone_number','email')})

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
     list_display=('user_id','username','leave_type','reason','status','start_date','end_date')
     readonly_fields=('user_id','username','leave_type','reason','start_date','end_date')
     exclude=('id',)
@admin.register(Employee)
class EmployeeRegisterAdmin(admin.ModelAdmin):
    list_display=('user','discord_user_id','job_title','phone_number')
    exclude=('id',)

@admin.register(BankDetails)
class BankDetailsRegisterAdmin(admin.ModelAdmin):
    list_display=('user','bank_name','bank_branch_location','employee_bank_account_name','employee_bank_account_number')
    exclude=('id',)