import json
import logging
from interface import DispatchableConnection
from multiuploader.models import MultiuploaderImage
from datetime import timedelta, datetime
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils.timezone import utc
from django.conf import settings
from django.utils.importlib import import_module
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
from django.contrib.auth import get_user_model
User = get_user_model()

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
        caption_ev = ""
        eventslug = ""

        if entry.event_date:
            caption_text.append("@ %s" %entry.event_date.event.title)
            caption_ev = "@ %s" %entry.event_date.event.title
            eventslug = "/events/" + entry.event_date.event.slug
        caption_text.append("by %s" % entry.userprofile.get_full_name())


        msg = {
            "image": entry.url,
            "id": entry.id,
            "timestamp": entry.upload_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            "caption_both": " ".join(caption_text),
            "caption_by": "by %s" % entry.userprofile.get_full_name(),
            "caption_ev": caption_ev,
            "userslug": "/profile/" + entry.userprofile.slug,
            "eventslug": eventslug,
            "favorited": entry.favorite_by.filter(user=self.user).count() != 0,
            "reported": entry.is_irrelevant or entry.is_inappropriate,
            "fgff" : "555888"
        }
        return msg

    def on_close(self):
        if self in PhotoStream.connected_users:
            PhotoStream.connected_users.remove(self)

    def on_open(self, info):
        PhotoStream.connected_users.add(self)
        if "sessionid" in info.cookies:
            sessionid = info.cookies["sessionid"].value
            session = SessionStore(session_key=sessionid)
        else:
            session = None

        if session and "_auth_user_id" in session:
            user = User.objects.get(pk=session["_auth_user_id"])
        else:
            user = None
        self.user = user

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
            self.send_message("prepend_entry", self.entry_serializer(entry))

    def on_fetch_latest(self, count=16):
        """
            fetches ``count`` latest photos from subscribed events or users
        """
        user_photos = Q(userprofile__slug__in=self.subscriptions["profiles"])
        event_photos = Q(event_date__event__slug__in=self.subscriptions["events"])

        objs = MultiuploaderImage.objects.filter(user_photos | event_photos).order_by('-upload_date')[:count]
        for obj in objs:
            self.send_message("append_entry", self.entry_serializer(obj))

    def on_fetch_more(self, offset=None, count=4):
        """
            fetches ``count`` more photos older than ``offset`` iso-timestamp
        """
        if not offset:
            return
        offset = parse_datetime(offset)
        user_photos = Q(userprofile__slug__in=self.subscriptions["profiles"])
        event_photos = Q(event_date__event__slug__in=self.subscriptions["events"])
        older = Q(upload_date__lt=offset)

        objs = MultiuploaderImage.objects.filter((user_photos | event_photos) & older).order_by('-upload_date')[:count]
        for obj in objs:
            self.send_message("append_entry", self.entry_serializer(obj))
        self.send_message("fetch_end", None)

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
