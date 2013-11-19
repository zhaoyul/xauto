from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.mail import EmailMessage

def render_subject(template, context=None):
    context = context or {}
    currentSite = Site.objects.get_current()
    context.update({
        'site': currentSite,
    })
    return ''.join(render_to_string(template, context).splitlines())

def render_message(template, context):
    context = context or {}
    current_site = Site.objects.get_current()
    context.update({
        'site': current_site,
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http',
        'MEDIA_URL': settings.MEDIA_URL,
    })
    return render_to_string(template, context)

def render_subject_message(subject, body, context):
    return render_subject(subject, context), render_message(body, context)

def django_send_mail(subject, message, recipient_list, priority='medium',
              from_email=None, fail_silently=False, mailer=True,
              **kwargs):
    """
    Send  text and html email using mailer, falling back to text-only
    django sending if mailer isn't used.
    
    subject,
    message,
    reply_info,
    (email,),
    headers = {
        'Reply-To': '%s' % reply_info.replace("\n", "").replace("\r", "")
    
    """

    #send_html_mail/send_mail needs to be imported here for testing emails.
    if settings.EMAIL_BACKEND[:13 ] == "django_mailer" and mailer==True:
        #from django_mailer_html import send_mail_html as send_mail
        from django_mailer import send_mail as send_mail
        use_mailer = True
    else:
        from django.core.mail import mail_managers as django_send_mail
        use_mailer = False

    if use_mailer:
        send_mail(subject, message, from_email, recipient_list)
        #mail_admins(subject, message_html)
        return True
    else:
        return commonHtmlEmail(subject, message, from_email, recipient_list,  fail_silently=fail_silently)

def commonHtmlEmail(subject, message, fromEmail, toEmail, fail_silently=True):
    if fail_silently:
        try:
            toEmail = toEmail
            msg = EmailMessage(subject, messageText, fromEmail, toEmail)
            return True
        except:
            return False
    else:
        # django.core.mail.backends.smtp
        toEmail = toEmail
        msg = EmailMessage(subject, message, fromEmail, toEmail)
        return True

