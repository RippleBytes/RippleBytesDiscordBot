from django.db import models
from django.utils.timezone import now

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
