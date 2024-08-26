from taskmanager.settings import *

CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache'
CELERY_CACHE_BACKEND = 'memory'
CELERY_TASK_ALWAYS_EAGER = True  # Run tasks locally instead of sending them to the worker
CELERY_TASK_EAGER_PROPAGATES = True  # Propagate exceptions raised by tasks