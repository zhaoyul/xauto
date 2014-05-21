from datetime import datetime
from django.conf import settings


def get_time_display(time):
    return datetime.strftime(time, settings.DATETIME_FORMAT)
