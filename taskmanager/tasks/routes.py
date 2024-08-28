"""DRF routes are stored here"""
from rest_framework.routers import DefaultRouter
from tasks.api_views import TaskViewSet, CategoryViewset

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewset)

urlpatterns = router.urls
