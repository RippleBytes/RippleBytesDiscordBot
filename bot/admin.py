from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import GroupAdmin,UserAdmin
from .models import CheckinRecord,TaskRecord,BreakRecord,LeaveRequest,BankDetail,User
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm,UserCreationForm,UserChangeForm
from unfold.contrib.import_export.forms import ImportForm,ExportForm
from unfold.admin import TabularInline,ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from unfold.views import UnfoldModelAdminViewMixin
from django.views.generic import TemplateView
from unfold.decorators import action
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken,OutstandingToken
from django.utils.html import format_html

admin.site.unregister(Group)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)


class TaskRecordInline(TabularInline):
    model=TaskRecord
    tab=True
    extra=0
    fields=['task','completed']
    readonly_fields=('task','completed',)

@admin.register(User)
class CustomAdmin(UserAdmin,ModelAdmin):
    fieldsets = [
        ('General', {
            'fields': [
                'discord_user_id', 'username', 'job_title',
                'date_of_birth', 'gender', 'last_login', 'phone_number','password',
                'email', 'private_email', 'employee_citizenship_number',
                'employee_citizenship_photo', 'employee_pp_photo', 'employee_resume_pdf'
            ],
        }),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    ]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                'discord_user_id', 'username', 'job_title',
                'date_of_birth', 'gender', 'last_login', 'phone_number','password',
                'email', 'private_email', 'employee_citizenship_number',
                'employee_citizenship_photo', 'employee_pp_photo', 'employee_resume_pdf'
            )}
         ),
    )
    form=UserChangeForm
    add_form=UserCreationForm
    change_password_form=AdminPasswordChangeForm

    inlines=[TaskRecordInline]
    readonly_fields=('discord_user_id','username','last_login')

@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(ModelAdmin):
    pass

@admin.register(OutstandingToken)
class OutstandingTokenAdmin(ModelAdmin):
    pass

@admin.register(Group)
class DjangoGroupAdmin(GroupAdmin,ModelAdmin):
    warn_unsaved_form=True

@admin.register(CheckinRecord)
class CheckinRecordAdmin(ModelAdmin,ImportExportModelAdmin):
    
    list_display = ('user','username', 'checkin_time', 'checkout_time')
    import_form_class=ImportForm
    export_form_class=ExportForm

@admin.register(TaskRecord)
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

@admin.register(BreakRecord)
class BreakRecordAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('checkin', 'start_time', 'end_time', 'reason','break_duration')
    import_form_class=ImportForm
    export_form_class=ExportForm
    list_filter=[
        ('start_time',RangeDateTimeFilter)
    ]
    def break_duration(self,obj):
        return (obj.end_time- obj.start_time)
    
    
    break_duration.short_description='Break Duration'


@admin.register(LeaveRequest)
class LeaveRequestAdmin(ModelAdmin,ImportExportModelAdmin):
     list_display=('user_id','username','leave_type','reason','status','start_date','end_date','leave_days')
     readonly_fields=('user_id','username','leave_type','reason','start_date','end_date')
     exclude=('id',)
     
     import_form_class=ImportForm
     export_form_class=ExportForm
     
     list_filter=[
         'leave_type',
         'status',
         ('start_date',RangeDateFilter)
     ]
     list_filter_submit=True
     def leave_days(self,obj):
        
         return (obj.end_date -obj.start_date).days
     
     leave_days.short_description='No of leave days'
     
     
@admin.register(BankDetail)
class BankDetailRegisterAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display=('user','bank_name','bank_branch_location','employee_bank_account_name','employee_bank_account_number')
    exclude=('id',)
    import_form_class=ImportForm
    export_form_class=ExportForm