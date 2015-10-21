from django.core.management.base import BaseCommand, CommandError
from subprocess import call


class Command(BaseCommand):
    help = 'Download image'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        call(
            "wget -O {0} {1}".format(options['path'], options['url']),
            shell=True)
