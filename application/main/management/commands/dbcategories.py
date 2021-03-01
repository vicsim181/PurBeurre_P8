import json
from django.core.management.base import BaseCommand, CommandError
from main.models import Category


class Command(BaseCommand):
    help = 'Create the categories in the main_category table.'

    def handle(self, *args, **options):
        with open('main/management/commands/categories.json', 'r') as categories:
            data = json.load(categories)
        for category_name in data['categories']:
            try:
                print(category_name)
                category = Category(name=category_name)
                category.save()
            except category.DoesNotExist:
                raise CommandError('No category in the CATEGORIES list.')
