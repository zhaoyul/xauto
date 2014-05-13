from django.db import models
from event.models import Currency, EventDate


def run():
    unique_fields = ['currency', 'symbol']

    duplicates = (Currency.objects.values(*unique_fields)
                                 .annotate(max_id=models.Max('id'),
                                           count_id=models.Count('id'))
                                 .filter(count_id__gt=1)
                                 .order_by())
    for duplicate in duplicates:
        # reassign to master
        master = Currency.objects.get(id=duplicate['max_id'])
        print 'Master currency is: ', master
        for dupe in Currency.objects.filter(**{x: duplicate[x] for x in unique_fields})\
            .exclude(id=duplicate['max_id']):
            print 'Duplicate found: ', dupe
            for ed in EventDate.objects.filter(currency=dupe):
                ed.currency = master
                ed.save()

        # remove dupes
        (Currency.objects.filter(**{x: duplicate[x] for x in unique_fields})
                        .exclude(id=duplicate['max_id'])
                        .delete())
