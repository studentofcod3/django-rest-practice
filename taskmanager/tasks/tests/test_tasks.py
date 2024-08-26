from django.test import TestCase
from model_bakery import baker
from tasks.tasks import send_task_creation_email
from tasks.models import Task

class CeleryTaskTest(TestCase):
    def test_send_task_creation_email(self):
        task = baker.make(Task)
        result = send_task_creation_email.delay(task.id)
        self.assertTrue(result.successful())