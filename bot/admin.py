from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from .models import CheckinRecord,TaskRecord,BreakRecord,LeaveRequest,BankDetail,User
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm,UserCreationForm,UserChangeForm
from unfold.contrib.import_export.forms import ImportForm,ExportForm
from unfold.admin import TabularInline
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from unfold.views import UnfoldModelAdminViewMixin
from django.views.generic import TemplateView
from unfold.decorators import action
from django.utils.translation import gettext_lazy as _
from .forms import RegistrationForm,CustomUserChangeForm




admin.site.unregister(Group)



class TaskRecordInline(TabularInline):
    model=TaskRecord
    tab=True
    fields=['task','completed']
    readonly_fields=('task','completed',)

@admin.register(User)
class CustomAdmin(ModelAdmin):
    fields=('discord_user_id','username','job_title','date_of_birth','gender','last_login','phone_number','email','private_email','employee_citizenship_number','employee_citizenship_photo','employee_pp_photo','employee_resume_pdf')

    inlines=[TaskRecordInline]
    readonly_fields=('discord_user_id','username','last_login')
    

    

    
@admin.register(Group)
class DjangoGroupAdmin(GroupAdmin,ModelAdmin):
    warn_unsaved_form=True


    

@admin.register(CheckinRecord)
class CheckinRecordAdmin(ModelAdmin,ImportExportModelAdmin):
    
    list_display = ('user','username', 'checkin_time', 'checkout_time')
    import_form_class=ImportForm
    export_form_class=ExportForm

   




class TaskRecordAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('user', 'task', 'completed')
    import_form_class=ImportForm
    export_form_class=ExportForm
    
    list_filter=['completed']
    actions=['set_status_completed','set_status_incomplete']
    
    @action(description="Change task status to complete")
    def set_status_completed(ModelAdmin,request,queryset):
        queryset.update(completed=True)


    @action(description="Change task status to incomplete")
    def set_status_incomplete(ModelAadmin,request,queryset):
        queryset.update(completed=False)



admin.site.register(TaskRecord,TaskRecordAdmin)

    

@admin.register(BreakRecord)
class BreakRecordAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('checkin', 'start_time', 'end_time', 'reason')
    import_form_class=ImportForm
    export_form_class=ExportForm
    list_filter=[
        ('start_time',RangeDateTimeFilter)


    ]

@admin.register(LeaveRequest)
class LeaveRequestAdmin(ModelAdmin,ImportExportModelAdmin):
     

     readonly_fields=('user','username','start_date','end_date','reason')
     list_display=('user','username','status','leave_type','reason','start_date','end_date')
    
     
     import_form_class=ImportForm
     export_form_class=ExportForm
     
     list_filter=[
         'leave_type',
         'status',
         ('start_date',RangeDateFilter)
     ]
     list_filter_submit=True
     
     
        
        

@admin.register(BankDetail)
class BankDetailRegisterAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display=('user','bank_name','bank_branch_location','employee_bank_account_name','employee_bank_account_number')
    exclude=('id',)
    import_form_class=ImportForm
    export_form_class=ExportForm