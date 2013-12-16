from django.core.management.base import BaseCommand, CommandError
from socket_streamer.main import run


class Command(BaseCommand):
    def handle(self, *args, **options):
        print "starting socket streamer"
        run()
