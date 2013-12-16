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

    def on_fetch_latest(self):
        now = datetime.now()
        objs = MultiuploaderImage.objects.filter(upload_date__gt=now-timedelta(days=1))
        for obj in objs:
            msg = {
                "url": obj.url,
                "id": obj.id
            }
            self.send_message("entry", msg)

    def on_favorite(self, id):
        print "favorited entry", id

    def on_report(self, id):
        print "reported entry", id
