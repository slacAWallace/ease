from __future__ import absolute_import, unicode_literals
from .celery import app

#Django setup
import os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'web_interface.settings'
django.setup()

from web_interface.alert_config_app.models import Alert, Trigger
from django.contrib.auth.models import User

@app.task
def add(x, y):
    return x + y


@app.task
def proc_alert(trigger_id=None):
    #Processes a triggered trigger: decides whether to send alerts, and sends them

    #Get the alert
    #Should we send an alert?
    #When was the last time we sent an alert?
    #Is the alert shelved?
    #Send an email
    #Send Slack
    #Mark the alert last sent
    pass

def make_alert_email():
    #Make the email to be sent
    pass

def send_email():
    pass

def send_slack():
    pass

