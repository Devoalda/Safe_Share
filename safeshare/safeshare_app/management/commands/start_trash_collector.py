from django.core.management.base import BaseCommand
from safeshare_app.utils.TrashCollector.TrashCollector import TrashCollector

class Command(BaseCommand):
    help = 'Start the trash collector'

    def handle(self, *args, **options):
        trash_collector = TrashCollector()
        trash_collector.start()
