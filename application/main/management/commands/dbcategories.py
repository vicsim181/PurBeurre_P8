from django.core.management.base import BaseCommand, CommandError
from main.models import Category


CATEGORIES = ["fromage", "yaourt", "fromage de vache", "fromage de chevre", "fromage bleu", "fromage tome", "camembert",
              "roquefort", "yaourt nature", "yaourt aux fruits", "yaourt soja", "glace chocolat", "glace vanille",
              "glace sorbet fruit", "biscuit", "biscuit chocolat", "biscuit beurre", "biscuit fruits", "soda",
              "soda cola", "limonade", "soda fruits", "charcuterie", "jambon", "saucisson"]


class Command(BaseCommand):
    help = 'Create the categories in the main_category table.'

    def handle(self, *args, **options):
        # print("c'est un bon début")
        for category_name in CATEGORIES:
            try:
                print(category_name)
                category = Category(name=category_name)
                category.save()
            except category.DoesNotExist:
                raise CommandError('No category in the CATEGORIES list.')
