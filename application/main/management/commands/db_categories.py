import json
from re import sub
from django.core.management.base import BaseCommand, CommandError
from main.models import Category, Store


class Command(BaseCommand):
    help = 'Create the categories in the main_category table.'

    def handle(self, *args, **options):
        unknown = Store(name="Lieu d'achat non précisé")
        unknown.save()
        with open('main/management/commands/settings.json', 'r') as settings:
            data = json.load(settings)
        categories = data['categories']
        for main_category in categories:
            self.create_category(main_category)
            for sub_category in categories[main_category]:
                self.create_category(sub_category)

    def create_category(self, category_name):
        try:
            print(category_name)
            category = Category(name=category_name)
            category.save()
        except category.DoesNotExist:
            raise CommandError('No category in the CATEGORIES list.')
