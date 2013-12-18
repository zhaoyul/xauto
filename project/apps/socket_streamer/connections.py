import json
import logging
from interface import DispatchableConnection
from multiuploader.models import MultiuploaderImage
from datetime import timedelta, datetime

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
            msg = {
                "url": entry.url,
                "id": entry.id
            }
            self.send_message("entry", msg)

    def on_fetch_latest(self):
        """
            fetches latest photos from subscribed events or users
        """
        now = datetime.now()

        # send latest followed users photos
        objs = MultiuploaderImage.objects.filter(userprofile__slug__in=self.subscriptions["profiles"])
        for obj in objs:
            msg = {
                "url": obj.url,
                "id": obj.id
            }
            self.send_message("entry", msg)

        # send latest photos in followed events
        objs = MultiuploaderImage.objects.filter(upload_date__gt=now-timedelta(days=1), event_date__event__slug__in=self.subscriptions["events"])
        for obj in objs:
            msg = {
                "url": obj.url,
                "id": obj.id
            }
            self.send_message("entry", msg)

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
