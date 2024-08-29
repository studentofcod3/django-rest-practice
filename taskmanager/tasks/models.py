from datetime import datetime
from django.db import models
from django_extensions.db.models import TimeStampedModel

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Task(TimeStampedModel):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField(default=datetime.now())
    description = models.TextField()
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
