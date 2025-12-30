from django.db import models

from signup.models import User

# Create your models here.

class Todo(models.Model):

    class PriorityChoices(models.TextChoices):
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    email = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.TextField()
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=6, choices=PriorityChoices.choices, default=PriorityChoices.MEDIUM)
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
