import json
import logging
from interface import DispatchableConnection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PhotoStream(DispatchableConnection):
    connected_users = dict()

    def __init__(self, *a, **kw):
        super(MessagesConnection, self).__init__(*a, **kw)

    def on_open(self, info):
        print "Connected",info
