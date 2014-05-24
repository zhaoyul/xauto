from django.db import models
from event.models import EventDate
from multiuploader.models import MultiuploaderImage


def run():
    """
    https://trello.com/c/WKwdzgbk/102-what-to-do-with-images-that-are-not-matched-to-any-events
    Assign 1040-1097 to Concorso Ferrari (id=73)
    58-281 Cars and Coffee Irvine Jan 11 (id=12)
    625-869 to Cars and Coffee Irvine Mar 15 (id=26)
    """

    try:
        ferrari = EventDate.objects.get(id=73)
        MultiuploaderImage.objects.filter(id__gte=1040, id__lte=1097).update(event_date=ferrari)
        print 'updated ferrari'
    except EventDate.DoesNotExist:
        print 'EventDate ferrari not found!'

    try:
        coffeirvine_11 = EventDate.objects.get(id=12)
        MultiuploaderImage.objects.filter(id__gte=58, id__lte=281).update(event_date=coffeirvine_11)
        print 'updated coffeirvine 11'
    except EventDate.DoesNotExist:
        print 'EventDate coffeirvine 11 not found!'

    try:
        coffeirvine_15 = EventDate.objects.get(id=26)
        MultiuploaderImage.objects.filter(id__gte=625, id__lte=869).update(event_date=coffeirvine_15)
        print 'updated coffeirvine 15'
    except EventDate.DoesNotExist:
        print 'EventDate coffeirvine 15 not found!'
