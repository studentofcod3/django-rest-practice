from django.contrib import admin
from tasks.models import Task, Category

admin.site.register(Task)
admin.site.register(Category)
