import discord
from discord.ext import commands
from django.core.management.base import BaseCommand
from bot.models import CheckinRecord, TaskRecord, BreakRecord,LeaveRequest,Employee
from django.utils.timezone import now
from django.db import transaction
from asgiref.sync import sync_to_async
import traceback
from datetime import datetime
from enum import Enum
import pytz
from django.conf import settings
DISCORD_TOKEN = settings.DISCORD_TOKEN
ADMIN_CHANNEL_ID=settings.ADMIN_CHANNEL_ID
LEAVE_CHANNEL_ID=settings.LEAVE_CHANNEL_ID




allowed_date_current=datetime.now().year
allowed_date_list=(allowed_date_current,(allowed_date_current+1))


    
def leave_type_value(leave_type):
    if leave_type=='1':
        leave_type='Unpaid Leave'
    elif leave_type=='2':
        leave_type='Annual Leave'
    elif leave_type=='3':
        leave_type='Sick Leave'
    else:
        leave_type='Unknown'
    return leave_type

def time_validation(start_date:datetime,end_date:datetime):
    if (start_date<datetime.now().date()):
        return False
    if (start_date.year not in allowed_date_list) and (end_date.year not in allowed_date_list):
        return False
    
    if (end_date < start_date):
        return False
    return True

format="%Y-%m-%d %H:%M:%S"
def time_converter(utc_time: datetime):

    if utc_time.tzinfo is None:
        utc_timezone = pytz.timezone('UTC')
        utc_time = utc_timezone.localize(utc_time)

    
    kathmandu_timezone = pytz.timezone('Asia/Kathmandu')
    kathmandu_time = utc_time.astimezone(kathmandu_timezone)

    
    formatted_time = kathmandu_time.strftime(format)  
    return formatted_time

class LeaveRequestStatus(Enum):
    requested='Requested',
    rejected='Rejected',
    approved='Approved'
    
    def __str__(self):
        return self.value
    


class CheckinModal(discord.ui.Modal, title="Check-in Tasks"):
    tasks = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="Tasks (One per line)",
        required=True,
        placeholder="Enter your tasks here, one per line",
        max_length=1500,
    )

    def __init__(self, user):
        super().__init__()
        self.user = user

    async def on_submit(self, interaction: discord.Interaction):
        tasks_input = self.tasks.value.strip()
        tasks = tasks_input.splitlines()

        # async with transaction.atomic():
        try:
            # Create CheckinRecord
            checkin_record = await sync_to_async(CheckinRecord.objects.create)(
                user_id=str(self.user.id),
                username=self.user.name,
                checkin_time=now()
            )

            # Create TaskRecords
            task_records = [
                TaskRecord(checkin=checkin_record, task=task.strip()) for task in tasks if task.strip()
            ]
            await sync_to_async(TaskRecord.objects.bulk_create)(task_records)

            embed = discord.Embed(
                title="Checkin",
                description=self.tasks.value,
                color=discord.Color.green()
            )
            embed.set_author(name=self.user.name)
            embed.add_field(name="Checkin Time", value=time_converter(checkin_record.checkin_time), inline=False)
            await interaction.channel.send(embed=embed)

            await interaction.response.send_message(
                "✅ Check-in successful!",
                ephemeral=True
            )
        except Exception as e:
            traceback.print_exc()
            await interaction.response.send_message(
                "❌ Check-in failed! Please try again.",
                ephemeral=True
            )

class BreakModal(discord.ui.Modal, title="Start Break"):
    reason = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="Reason for Break",
        required=True,
        placeholder="Enter the reason for your break",
        max_length=500,
    )

    def __init__(self, user, checkin_record):
        super().__init__()
        self.user = user
        self.checkin_record = checkin_record

    async def on_submit(self, interaction: discord.Interaction):
        reason_input = self.reason.value.strip()

        try:
            # Create BreakRecord
            break_record = await sync_to_async(BreakRecord.objects.create)(
                checkin=self.checkin_record,
                start_time=now(),
                reason=reason_input
            )

            embed = discord.Embed(
                title="Break Start",
                description=self.reason.value,
                color=discord.Color.yellow()
            )
            embed.set_author(name=self.user.name)
            embed.add_field(name="Break Taken Time", value=time_converter(break_record.start_time), inline=False)
            await interaction.channel.send(embed=embed)

            await interaction.response.send_message(
                "✅ Break started!",
                ephemeral=True
            )
        except Exception as e:
            traceback.print_exc()
            await interaction.response.send_message(
                "❌ Failed to start break! Please try again.",
                ephemeral=True
            )

class CheckoutModal(discord.ui.Modal, title="Checkout"):
    tasks_completed = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="Completed Tasks (One per line)",
        required=False,
        placeholder="Enter completed tasks here, one per line",
        max_length=1500,
    )
    additional_tasks = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="Additional Tasks (Optional, one per line)",
        required=False,
        placeholder="Enter additional tasks here, one per line",
        max_length=1500,
    )

    def __init__(self, user, checkin_record):
        super().__init__()
        self.user = user
        self.checkin_record = checkin_record

    async def on_submit(self, interaction: discord.Interaction):
        tasks_completed_input = self.tasks_completed.value.strip()
        additional_tasks_input = self.additional_tasks.value.strip()

        completed_tasks = tasks_completed_input.splitlines() if tasks_completed_input else []
        additional_tasks = additional_tasks_input.splitlines() if additional_tasks_input else []

        try:
            # Mark existing tasks as completed
            for task in completed_tasks:
                await TaskRecord.objects.filter(
                    checkin=self.checkin_record, task__iexact=task.strip()
                ).aupdate(completed=True)

            # Add additional tasks as completed
            new_task_records = [
                TaskRecord(checkin=self.checkin_record, task=task.strip(), completed=True)
                for task in additional_tasks if task.strip()
            ]
            if new_task_records:
                await sync_to_async(TaskRecord.objects.bulk_create)(new_task_records)

            # Set checkout time
            self.checkin_record.checkout_time = now()
            await sync_to_async(self.checkin_record.save)()

            embed = discord.Embed(
                title="Checkout",
                description=self.tasks_completed.value,
                color=discord.Color.blue()
            )
            embed.set_author(name=self.user.name)
            embed.add_field(name="Additional Task Completed", value=self.additional_tasks.value, inline=False)
            embed.add_field(name="Checkout Time", value=time_converter(self.checkin_record.checkout_time), inline=False)
            await interaction.channel.send(embed=embed)

            await interaction.response.send_message(
                "✅ Checkout successful! Have a great day!",
                ephemeral=True
            )
        except Exception as e:
            traceback.print_exc()
            await interaction.response.send_message(
                "❌ Checkout failed! Please ensure task names are correct and try again.",
                ephemeral=True
            )


class LeaveRequestModal(discord.ui.Modal,title='LeaveRequest'):  
   

    reason=discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='Request leave',
        required=True,
        placeholder='State the reason of leave',
        max_length=100,
    )
    

    leave_type=discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="1.Sick Leave 2.Annual Leave 3.Unpaid Leave",
        required=False,
        placeholder='Mention the type of leave(1-3). Blank for annual Leave ',
        max_length=1
    )

    start_date=discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='Start Date(YYYY/MM/DD)',
        required=True,
        placeholder='Enter the starting date of leave',
        max_length=10
    )


    end_date=discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='End Date(YYYY/MM/DD)',
        required=True,
        placeholder='Enter the ending date of leave',
        max_length=10,
    )


    def __init__(self,user):
        super().__init__()
        self.user=user
    
    

    

    async def on_submit(self, interaction:discord.Interaction):
        reason_input=self.reason.value.strip()
        leave_type_inpt=self.leave_type.value.strip()
        leave_type=leave_type_value(leave_type_inpt)
        date_format='%Y/%m/%d'
    
        start_date=datetime.strptime(self.start_date.value,date_format).date()
        end_date=datetime.strptime(self.end_date.value,date_format).date()
        # leave_type=self.add_item(DropDown)
        if time_validation(start_date,end_date):
                try:
                        leave_request=await sync_to_async(LeaveRequest.objects.create)(
                            user_id=str(self.user.id),
                            username=self.user.name,
                            reason=reason_input,
                            leave_type=leave_type,
                            start_date=start_date,
                            end_date=end_date
                        )

                        embed=discord.Embed(
                            title="Leave request initiated",
                            color=discord.Color.orange(),
                            description=reason_input
                        )

                        
                        embed.set_author(name=self.user.name)
                        embed.add_field(name='Leave request starting from' , value=leave_request.start_date,inline=False)
                        embed.add_field(name='Leave request till',value=leave_request.end_date)
                        embed.add_field(name="No. of Leave Days :",value=(leave_request.end_date-leave_request.start_date).days+1,inline=False)

                        
                        channel=interaction.guild.get_channel(int(ADMIN_CHANNEL_ID))
                        #ADMIN_CHANNEL_ID needs to be converted into int, else return NONE
                        
                        await channel.send(embed=embed)

                        
                        await interaction.response.send_message(
                            "✅ Leave request sent successfully!",ephemeral=True
                        ) 
                   
                except Exception as e:
                    
                        traceback.print_exc()
                        await interaction.response.send_message(
                            "❌ Failed to initiate a request ! Please try again.",
                            ephemeral=True
                        )
        else:
            await interaction.response.send_message(
                "❌ Failed to initiate a request ! Please provide valid dates"
            )
                

class Command(BaseCommand):
    help = "Run the Discord bot"
    def handle(self, *args, **options):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        bot = commands.Bot(command_prefix="!", intents=intents)

        bot = commands.Bot(command_prefix="!",intents=intents)
        

        @bot.event
        async def on_ready():
            self.stdout.write(self.style.SUCCESS(f'Logged in as {bot.user} (ID: {bot.user.id})'))
            await bot.tree.sync()
            self.stdout.write(self.style.SUCCESS("Bot is ready and commands are synced."))

        


        
        @bot.tree.command(name="checkin", description="Start your check-in by entering your tasks.")
        async def checkin(interaction: discord.Interaction):
            existing_record = await CheckinRecord.objects.filter(
                user_id=str(interaction.user.id), checkout_time__isnull=True
            ).afirst()
            if existing_record:
                await interaction.response.send_message(
                    "❌ You already have an active check-in! Please checkout first.",
                    ephemeral=True
                )
            else:
                modal = CheckinModal(interaction.user)
                await interaction.response.send_modal(modal)
        

        #create slash commands
        
        @bot.tree.command(name='leave_request',description="Send a leave request to admin")
        async def take_leave(interaction:discord.Interaction):
            
            channel=bot.get_channel(ADMIN_CHANNEL_ID)
        
            # await channel.send('admin')
            # channel=bot.get_channel(1314130782503043103)
            # channel=bot.get_channel(1314130782503043103)
        
            # await channel.send('admin')
            leave_request= await LeaveRequest.objects.filter(
                
                user_id=str(interaction.user.id)
            ).afirst()
            # await channel.send('admin heloo.')
            
                
            modal=LeaveRequestModal(interaction.user)
            await interaction.response.send_modal(modal)
            
            
                


        @bot.tree.command(name="checkout", description="Checkout by marking completed tasks and adding any additional tasks.")
        async def checkout(interaction: discord.Interaction):
            checkin_record = await CheckinRecord.objects.filter(
                user_id=str(interaction.user.id), checkout_time__isnull=True
            ).afirst()
            if not checkin_record:
                await interaction.response.send_message(
                    "❌ No active check-in found. Please check in first.",
                    ephemeral=True
                )
            else:
                modal = CheckoutModal(interaction.user, checkin_record)
                # Optionally, pre-fill the placeholder with existing task names
                existing_tasks = []
                async for task in TaskRecord.objects.filter(checkin=checkin_record):
                    existing_tasks.append(task.task)
                modal.tasks_completed.default = f"\n".join(existing_tasks)
                await interaction.response.send_modal(modal)

        @bot.tree.command(name="take_break", description="Start a break by providing a reason.")
        async def take_break(interaction: discord.Interaction):
            checkin_record = await CheckinRecord.objects.filter(
                user_id=str(interaction.user.id), checkout_time__isnull=True
            ).afirst()
            if not checkin_record:
                await interaction.response.send_message(
                    "❌ You must check in before taking a break!",
                    ephemeral=True
                )
            else:
                # Check if there's already an ongoing break
                ongoing_break = await BreakRecord.objects.filter(
                    checkin=checkin_record, end_time__isnull=True
                ).afirst()
                if ongoing_break:
                    await interaction.response.send_message(
                        "❌ You already have an ongoing break!",
                        ephemeral=True
                    )
                else:
                    modal = BreakModal(interaction.user, checkin_record)
                    await interaction.response.send_modal(modal)

        @bot.tree.command(name="end_break", description="End your current break.")
        async def end_break_cmd(interaction: discord.Interaction):
            checkin_record = await CheckinRecord.objects.filter(
                user_id=str(interaction.user.id), checkout_time__isnull=True
            ).afirst()
            if not checkin_record:
                await interaction.response.send_message(
                    "❌ You must check in before ending a break!",
                    ephemeral=True
                )
            else:
                # Find the ongoing break
                ongoing_break = await BreakRecord.objects.filter(
                    checkin=checkin_record, end_time__isnull=True
                ).afirst()
                if not ongoing_break:
                    await interaction.response.send_message(
                        "❌ No active break found to end!",
                        ephemeral=True
                    )
                else:
                    try:
                        ongoing_break.end_time = now()
                        await sync_to_async(ongoing_break.save)()

                        embed = discord.Embed(
                            title="Break End",
                            description="Back to Work",
                            color=discord.Color.green()
                        )
                        embed.set_author(name=interaction.user.name)
                        embed.add_field(name="Break End Time", value=time_converter(ongoing_break.end_time), inline=False)
                        await interaction.channel.send(embed=embed)

                        await interaction.response.send_message(
                            "✅ Break ended successfully!",
                            ephemeral=True
                        )
                    except Exception as e:
                        traceback.print_exc()
                        await interaction.response.send_message(
                            "❌ Failed to end the break! Please try again.",
                            ephemeral=True
                        )

        @bot.tree.command(name="user_register",description='Create an employee login account!')
        async def user_login_cmd(interaction:discord.Interaction):
            await interaction.response.send_message("[Visit the register page](http://127.0.0.1:8000/register)",ephemeral=True)
        # Run the bot
        bot.run(DISCORD_TOKEN)
