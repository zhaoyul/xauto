from django.db import models
from django.utils.timezone import utc

import datetime

class TimestampedModel(models.Model):
    """
    A model baseclass adding 'created at' and 'last modified at'
    fields to models.
    """
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    class Meta:
        abstract = True

    def save(self, **kwargs):
        """
        On save, update timestamps
        """
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if not self.id:
            self.created = now
        self.modified = now
        super(TimestampedModel, self).save(**kwargs)
