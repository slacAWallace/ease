from celery import Celery

app = Celery('alert_dispatch_toolkit', broker='amqp://guest@localhost//')

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

