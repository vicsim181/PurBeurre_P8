import requests
import json
import pprint
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from main.models import Category, Product, Store


class Command(BaseCommand):
    help = 'Collect all the categories present in the category table of the database.\
            It then collects the data according to these categories via the OFF API.'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        with open('main/management/commands/settings.json', 'r') as settings:
            data = json.load(settings)
        url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1"
        for category in categories:
            parameters = {'search_terms': category.name, 'page_size': data['page_size'], 'page': data['page'],
                          'fields': data['fields']}
            try:
                r = requests.get(url=url, params=parameters)
                result = r.json()
            except json.decoder.JSONDecodeError:
                print('The json file returned from Open Food Facts is empty! It can be due to a HTTP error,\
                       check the url passed in requests and its parameters.')
                exit()
            except requests.exceptions.ConnectionError:
                print('A connection error occured')
                exit()
            raw_products = result['products']
            try:
                for raw_product in raw_products:
                    product = Product(code=raw_product['code'],
                                      name=raw_product['product_name'],
                                      nutriscore=raw_product['nutriscore_grade'],
                                      description=raw_product['ingredients_text'],
                                      url=raw_product['url'],
                                      popularity=raw_product['unique_scans_n'])
                    product.save()
            except IntegrityError:
                product = Product.objects.get(code=raw_product['code'])
                product.category.add(category)
                if raw_product['stores_tags']:
                    for store in raw_product['stores_tags']:
                        store = Store(name=store)
                        store.save()
                        product.store.add(store)
