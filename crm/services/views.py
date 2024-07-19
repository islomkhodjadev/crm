from django.shortcuts import render

# Create your views here.





from celery import Celery

app = Celery(broker='amqp://guest:guest@localhost:5672//')
  
    
def send_sms(request, _from, to, body):
    # Ensure the task name matches and arguments are passed correctly
    return app.send_task('send_sms', kwargs={'to_number': to, 'from_number': _from, 'body': body})

# send_sms(1, _from="+16592373136", to="+998993691864", body="hello Egambergan")



