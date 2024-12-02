from django.contrib import admin

from bot.models import CheckinRecord,TaskRecord,BreakRecord

@admin.register(CheckinRecord)
class CheckinRecordAdmin(admin.ModelAdmin):
    list_display = ('username', 'checkin_time', 'checkout_time')

@admin.register(TaskRecord)
class TaskRecordAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'task', 'completed')

@admin.register(BreakRecord)
class BreakRecordAdmin(admin.ModelAdmin):
    list_display = ('checkin', 'start_time', 'end_time', 'reason')

