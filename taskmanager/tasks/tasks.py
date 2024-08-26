from celery import shared_task
from django.core.mail import send_mail
from tasks.models import Task

@shared_task
def send_task_creation_email(task_id):
    task = Task.objects.get(id=task_id)
    send_mail(
        subject='New Task Created', 
        message=f'Task "{task.title}" has been created.', 
        from_email='ayyoub.maknassa@gmail.com', 
        recipient_list=['ayyoub.maknassa@gmail.com']
    )