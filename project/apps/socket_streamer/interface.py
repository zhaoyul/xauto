import json
import logging
from sockjs.tornado import SockJSConnection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Dispachable(object):
    def __init__(self, *a, **kw):
        self.dispatcher = {}
        for member in self.__class__.__dict__:
            if member.startswith("on_"):
                self.dispatcher[member[3:]] = getattr(self, member)

    def undispatched(self, name, *args, **kwargs):
        logger.info("Undispatched message %s (args: %s, kwargs: %s)" % (name,args,kwargs))

    def dispatch(self, name, *args, **kwargs):
        #handler = self.dispatcher.get(name, None)
        callback = "on_%s" % name
        if hasattr(self, callback):
            return getattr(self, callback)(*args, **kwargs)
        else:
            return self.undispatched(name, *args, **kwargs)


class DispatchableConnection(SockJSConnection, Dispachable):
    def __init__(self, *a, **kw):
        super(DispatchableConnection, self).__init__(*a, **kw)

    def on_open(self, info):
        logger.debug("Client connected: %s" % info.ip)

    def on_message(self, msg):
        try:
            if type(msg) == dict:
                message = msg
            else:
                message = json.loads(msg)
            if "type" in message:
                kwargs = {}
                if "data" in message:
                    kwargs = message["data"]
                self.dispatch(message["type"], **kwargs)
            else:
                logger.debug("Received unknown message: %s" % msg)
                return
        except Exception as e:
            logger.exception(e)
