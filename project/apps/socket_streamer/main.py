#!/usr/bin/env python
from tornado import web, autoreload, ioloop
from sockjs.tornado import SockJSRouter
from django.conf import settings
from multiuploader.models import MultiuploaderImage
from django.db.models import Max
from datetime import timedelta

import connections


def run():
    router = SockJSRouter(connections.PhotoStream, settings.SOCKET_STREAMER_URL)

    handlers = router.urls

    runtime_vars = dict()

    runtime_vars["last_obj_count"] = None
    runtime_vars.update(MultiuploaderImage.objects.aggregate(last_upload=Max('upload_date')))

    def db_periodic_check(*a, **kw):
        obj_count = MultiuploaderImage.objects.count()
        if obj_count != runtime_vars["last_obj_count"]:
            runtime_vars["last_obj_count"] = obj_count
            if not runtime_vars["last_upload"] is None:
                objs = MultiuploaderImage.objects.filter(upload_date__gt=runtime_vars["last_upload"])
                runtime_vars.update(MultiuploaderImage.objects.aggregate(last_upload=Max('upload_date')))
                for obj in objs:
                    for user in connections.PhotoStream.connected_users:
                        user.notify_new_entry(obj)

    app = web.Application(handlers)
    app.listen(int(settings.SOCKET_STREAMER_PORT), "0.0.0.0")
    ioloop.PeriodicCallback(db_periodic_check, 5000).start()
    autoreload.start(ioloop.IOLoop.instance())
    print "socket streamer is (re)started"
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        return
