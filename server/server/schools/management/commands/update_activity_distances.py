from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Updates the activity distance cache for schools"

    def add_arguments(self, parser):
        "parser.add_argument('some_number', nargs='+', type=int)"
        pass

    def create_all(self, entitiesPrefix=""):
        pass

    def handle(self, *args, **options):
        self.create_all()
