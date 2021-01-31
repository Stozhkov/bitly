from django.core.management.base import BaseCommand
from core.models import Link


class Command(BaseCommand):
    help = 'Delete old links from db'

    def handle(self, *args, **options):
        Link.delete_old_records()
