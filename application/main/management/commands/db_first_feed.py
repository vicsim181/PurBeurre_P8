from django.db.utils import DataError
import requests
import json
import pprint
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from main.models import Category, Product, Store, History


class Command(BaseCommand):
    help = 'Collect all the categories present in the category table of the database.\
            It then collects the data according to these categories via the OFF API.'

    def handle(self, *args, **options):
        """
        Function preparing the url and the parameters for the request.
        It collects the categories already in the database main_category table.
        Depending on the category (main one or sub one) the page_size will vary.
        It then calls the extract_data() function to perform the extraction.
        """
        try:
            last_page = History.objects.latest('date')
            page = last_page.page_number + 1
        except ObjectDoesNotExist:
            page = 1
        print('page: ' + str(page))
        categories = Category.objects.all()
        if not categories:
            print('The main_category table is empty, please feed it first to extract the categories.')
            return
        with open('main/management/commands/settings.json', 'r') as settings:
            data = json.load(settings)
        self.url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1"
        for category in categories:
            if category.name in data["categories_main"]:
                self.parameters = {'search_terms': category.name, 'page_size': data['page_size_main'], 'page': page,
                                   'fields': data['fields']}
            elif category.name in data["categories_sub"]:
                self.parameters = {'search_terms': category.name, 'page_size': data['page_size_sub'], 'page': page,
                                   'fields': data['fields']}
            self.extract_data(category)
        history = History(page_number=page)
        history.save()

    def extract_data(self, category):
        """
        Function called by the above one to perform the extraction of data on OpenFoodFacts.
        The searched category, the url and the parameters of the request are passed in as arguments.
        """
        try:
            r = requests.get(url=self.url, params=self.parameters)
            print('NOUVELLE REQUETE: ' + r.url)
            result = r.json()
        except json.decoder.JSONDecodeError:
            raise Exception('The json file returned from Open Food Facts is empty! It can be due to a HTTP error, \
check the url passed in requests and its parameters.')
        except requests.exceptions.ConnectionError:
            raise Exception('A connection error occured')
        raw_products = result['products']
        for raw_product in raw_products:
            self.treat_data(raw_product, category)

    def treat_data(self, raw_product, category):
        """
        Function that inserts a new product in the database if it's not already in.
        It also adds links between products and their categories and stores.
        """
        try:
            product = Product(code=raw_product['code'],
                              name=raw_product['product_name'],
                              nutriscore=raw_product['nutriscore_grade'],
                              description=raw_product['ingredients_text'],
                              url=raw_product['url'],
                              popularity=raw_product['unique_scans_n'])
            product.save()
            if raw_product['stores_tags']:
                stores = [store.replace('-', ' ') for store in raw_product['stores_tags']]
                if stores:
                    for store_element in stores:
                        try:
                            store = Store(name=store_element)
                            store.save()
                            product.store.add(store)
                            print('DONE: ' + store.name)
                        except DataError:
                            print('STORE DATAERROR')
                        except IntegrityError:
                            store = Store.objects.get(name=store_element)
                            product.store.add(store)
            product.category.add(category)
            print('DONE: ' + product.name)
        except KeyError:
            print('KEYERROR')
        except DataError:
            print('DATAERROR')
        except IntegrityError:
            print('DEJA DANS BDD ' + raw_product['product_name'])
            product = Product.objects.get(code=raw_product['code'])
            product.category.add(category)
