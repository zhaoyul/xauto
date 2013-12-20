import json
import logging
from interface import DispatchableConnection
from multiuploader.models import MultiuploaderImage
from datetime import timedelta, datetime
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils.timezone import utc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PhotoStream(DispatchableConnection):
    connected_users = set()

    def __init__(self, *a, **kw):
        super(PhotoStream, self).__init__(*a, **kw)
        self.subscriptions = {
            "profiles": [],
            "events": []
        }

    def send_message(self, type, data):
        msg = {
            'type': type,
            'data': data
        }
        self.send(json.dumps(msg))

    def entry_serializer(self, entry):
        """
            makes json from MultiuploaderImage
        """
        caption_text = []
        caption_text.append(entry.upload_date.strftime("%d %b %H:%M"))
        if entry.event_date:
            caption_text.append("@ %s" %entry.event_date.event.title)
        caption_text.append("by %s" % entry.userprofile.get_full_name())
        msg = {
            "image": entry.url,
            "id": entry.id,
            "timestamp": entry.upload_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "caption": " ".join(caption_text)
        }
        return msg

    def on_close(self):
        if self in PhotoStream.connected_users:
            PhotoStream.connected_users.remove(self)

    def on_open(self, info):
        PhotoStream.connected_users.add(self)

    def on_subscribe(self, subscriptions):
        """
            checks and saves user subscriptions
        """
        if "profiles" in subscriptions and "events" in subscriptions:
            self.subscriptions = subscriptions

    def notify_new_entry(self, entry):
        """
            reacts to new entry sending it to user if it is subscribed to
            poster or event
        """
        passing = False
        if entry.userprofile and entry.userprofile.slug in self.subscriptions["profiles"]:
            passing = True
        if entry.event_date and entry.event_date.event.slug in self.subscriptions["events"]:
            passing = True
        if passing:
            self.send_message("entry", self.entry_serializer(entry))

    def on_fetch_latest(self, count=16):
        """
            fetches ``count`` latest photos from subscribed events or users
        """
        now = datetime.utcnow().replace(tzinfo=utc)

        user_photos = Q(userprofile__slug__in=self.subscriptions["profiles"])
        event_photos = Q(event_date__event__slug__in=self.subscriptions["events"])

        objs = MultiuploaderImage.objects.filter(user_photos | event_photos).order_by('-upload_date')[:count]
        for obj in objs:
            self.send_message("append_entry", self.entry_serializer(obj))

    def on_fetch_more(self, offset, count=4):
        """
            fetches ``count`` more photos older than ``offset`` iso-timestamp
        """
        offset = parse_datetime(offset)
        user_photos = Q(userprofile__slug__in=self.subscriptions["profiles"])
        event_photos = Q(event_date__event__slug__in=self.subscriptions["events"])
        older = Q(upload_date__lte=offset)

        objs = MultiuploaderImage.objects.filter((user_photos | event_photos) & older).order_by('-upload_date')[:count]
        for obj in objs:
            self.send_message("append_entry", self.entry_serializer(obj))


    def on_favorite(self, id):
        """
            it will be handled by api
        """
        print "favorited entry", id

    def on_report(self, id):
        """
            it will be handled by api
        """
        print "reported entry", id
