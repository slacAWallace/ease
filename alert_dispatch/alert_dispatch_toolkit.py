from __future__ import absolute_import, unicode_literals
from .celery import app

from datetime import datetime

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
def proc_alert(alert_id=None, trigger_id=None):
    #Processes a triggered trigger: decides whether to send alerts, and sends them

    #Get the alert and trigger
    alert = Alert.objects.get(id=alert_id)
    trigger = Trigger.objects.get(id=trigger_id)
    #Should we send an alert?
    #When was the last time we sent an alert?
    if datetime.now() - alert.last_sent.datetime() > alert.lockout_duration.timedelta() and
    #Is the alert shelved?
    not alert.state() == Alert.SHELVED:
        send_alert = True
    else:
        send_alert = False

    #Send an email
    if send_alert and alert.use_email():
        email = make_alert_email()
        send_email(email)

    #Send Slack
    if send_alert and alert.use_slack():
        send_slack()

    #Mark the alert last sent
    alert.last_sent(datetime.now())
    

def make_alert_email():
    #Make the email to be sent
    pass

def send_email():
    pass

def send_slack():
    pass

