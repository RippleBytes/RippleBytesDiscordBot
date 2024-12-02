import discord
from discord.ext import commands
from django.core.management.base import BaseCommand
from bot.models import CheckinRecord, TaskRecord, BreakRecord
from django.utils.timezone import now
from django.db import transaction
from asgiref.sync import sync_to_async
import traceback

from django.conf import settings
DISCORD_TOKEN = settings.DISCORD_TOKEN

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
            embed.add_field(name="Checkin Time (UTC)", value=checkin_record.checkin_time, inline=False)
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
            embed.add_field(name="Break Taken Time (UTC)", value=break_record.start_time, inline=False)
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
            embed.add_field(name="Checkout Time (UTC)", value=self.checkin_record.checkout_time, inline=False)
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

class Command(BaseCommand):
    help = "Run the Discord bot"

    def handle(self, *args, **options):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        bot = commands.Bot(command_prefix="!", intents=intents)

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
                        embed.add_field(name="Break End Time (UTC)", value=ongoing_break.end_time, inline=False)
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

        # Run the bot
        bot.run(DISCORD_TOKEN)
