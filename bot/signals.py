from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveRequest
from asgiref.sync import async_to_sync
from .utils import send_discord_message
import json
from datetime import datetime as dt
from .management.commands import runbot
format="%Y-%m-%d "
@receiver(post_save,sender=LeaveRequest)
def leave_request_status_updated(sender,instance,created,**kwargs):
    if not created:
        if instance.status=='Approved':
            discord_channel_message={
                    "embeds": 
                    [
                        {
                            "color": 16711680,
                            "fields": [
                                {
                                "name": 'Leave for',
                                "value": instance.username,
                                "inline": False,
                                },
                                {
                                "name": 'Leave from',
                                "value": dt.strftime(instance.start_date,format),
                                "inline": True,
                                },
                                {
                                "name": 'Leave till',
                                "value": dt.strftime(instance.end_date,format),
                                "inline": True,
                                },
                                
                                {
                                    'name':'No of leave days',
                                    'value':(instance.end_date-instance.start_date).days,
                                    'inline': False
                                }             
                            ],
                        }
                    ]
            }

            send_discord_message(discord_channel_message)
           
        elif instance.status=='Rejected':
            pass
        else:
            pass
