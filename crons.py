# -*- coding: utf-8 -*-

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ordr.prod")
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker_background_tasks import conn_background_tasks
import logging
import sys
import random
from utils.customer_order_utils import execute_create_customer_invoice

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


sched = BlockingScheduler()

q_background = Queue(connection=conn_background_tasks)


# CHECK FOR DONE ORDERS
@sched.scheduled_job('interval', minutes=10)
def finished_crons():
    q_background.enqueue(execute_create_customer_invoice, timeout=600)


sched.start()
