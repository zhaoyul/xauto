from celery.task import Task, PeriodicTask
from celery.registry import tasks
from utils import log
from utils.email import django_send_mail
from django.conf import settings


class sendXautoEmails(Task):
    #queue = 'Recalculation'

    def run(self, subject, message, emailTo, from_email=settings.DEFAULT_FROM_EMAIL, **kwargs):
        
        django_send_mail(subject, message, emailTo, from_email=settings.DEFAULT_FROM_EMAIL)
        
        log.tofile('Celery_Task_%s' % 'auth', 'Run Task for [%s] for Auth[%s]' % ('sendxautoEmails', emailTo))
            
            
tasks.register(sendXautoEmails)
