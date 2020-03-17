from __future__ import absolute_import, unicode_literals

from config.celery import app_task, shared_task

# @shared_task
@app_task
def say_hello():
    print("hellow world!")