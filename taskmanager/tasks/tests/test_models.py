from django.test import TestCase
from model_bakery import baker
from tasks.models import Task, Category

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = baker.make(Category)
        self.assertIsInstance(category, Category)
        self.assertTrue(Category.objects.filter(id=category.id).exists())


class TaskModelTest(TestCase):
    def setUp(self):
        self.category = baker.make(Category)

    def test_task_creation(self):
        task = baker.make(Task, category=self.category)
        self.assertEqual(task.category, self.category)
        self.assertIsInstance(task, Task)
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_task_default_completed(self):
        task = baker.make(Task, category=self.category, completed=False)
        self.assertFalse(task.completed)

    def test_task_category_relationship(self):
        task = baker.make(Task, category=self.category)
        self.assertEqual(task.category, self.category)
        self.assertEqual(self.category.tasks.first(), task)
