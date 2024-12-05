from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .forms import Userregistrationform
from bot.models import CheckinRecord,TaskRecord,BreakRecord,LeaveRequest #,UserRegistration

class MediaInline(admin.TabularInline):
    model=TaskRecord
    fields=['task','completed']
    readonly_fields=('task','completed',)

@admin.register(CheckinRecord)
class CheckinRecordAdmin(admin.ModelAdmin):
    list_display = ('username', 'checkin_time', 'checkout_time')
    inlines=[MediaInline]

@admin.register(TaskRecord)
class TaskRecordAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'task', 'completed')

@admin.register(BreakRecord)
class BreakRecordAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'start_time', 'end_time', 'reason')

# class EmployeeAdmin(UserAdmin):
#     model=UserRegistration
#     form=Userregistrationform
#     fieldsets=(None,{'fields':('user_id','user_name','full_name','phone_number','email')})

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
     list_display=('user_id','username','leave_type','reason','status','start_date','end_date')
