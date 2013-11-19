from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from utils.email import django_send_mail

from celery.task import Task, PeriodicTask
from celery.registry import tasks

from utils import log
from django.conf import settings


class HtmlEmailSender(Task):
    #queue = 'Email'

    
    def run(self, subject, message, reply_info, emails):
        for email in emails:
            # ---- call django mailer ----
            log.tofile('Celery_Task_%s' % 'utils', 'Starting Task for [%s] for email[%s]' % ('HtmlEmailSender', email), enabled=settings.ENABLE_CELERY_LOGGING)
            django_send_mail(subject, message, (email,), from_email=reply_info)
            log.tofile('Celery_Task_%s' % 'utils', 'Completed Task for [%s] for email[%s]' % ('HtmlEmailSender', email), enabled=settings.ENABLE_CELERY_LOGGING)

class TxtEmailSender(Task):
    #queue = 'Email'

    
    def run(self, subject, message, reply_info, emails):
        for email in emails:
            log.tofile('Celery_Task_%s' % 'utils', 'Starting Task for [%s] for email[%s]' % ('TxtEmailSender', email), enabled=settings.ENABLE_CELERY_LOGGING)
            django_send_mail(subject, message, (email,), from_email=reply_info)
            log.tofile('Celery_Task_%s' % 'utils', 'Completed Task for [%s] for email[%s]' % ('TxtEmailSender', email), enabled=settings.ENABLE_CELERY_LOGGING)
            
tasks.register(HtmlEmailSender)
tasks.register(TxtEmailSender)

