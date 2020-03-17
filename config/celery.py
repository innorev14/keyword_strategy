from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config', broker='amqp://guest:guest@localhost//')  # amqp://guest:guest@localhost//  django://

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# v4.0 이상 일 경우
app.config_from_object('django.conf:settings', namespace='CELERY')
# v3.1 일 경우
# app.config_from_object('django.conf:settings')

# task 자동 탐색
# v4.0 이상 일 경우
app.autodiscover_tasks()
# v3.1 일 경우
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    # CELERYBEAT_SCHEDULE = {
    #     'say_hello-every-seconds': {
    #         "task": "App.tasks.CheckSite",
    #         'schedule': timedelta(seconds=30),
    #         'args': ()
    #     },
    # }
)