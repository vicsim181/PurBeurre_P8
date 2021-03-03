import json
from django.core.management.base import BaseCommand, CommandError
from main.models import Category


class Command(BaseCommand):
    help = 'Create the categories in the main_category table.'

    def handle(self, *args, **options):
        with open('main/management/commands/settings.json', 'r') as categories:
            data = json.load(categories)
        for category_name in data['categories_main']:
            self.create_categories(category_name)
        for category_name in data['categories_sub']:
            self.create_categories(category_name)

    def create_categories(self, category_name):
        try:
            print(category_name)
            category = Category(name=category_name)
            category.save()
        except category.DoesNotExist:
            raise CommandError('No category in the CATEGORIES list.')