from django.db.utils import DataError
import requests
import json
import pprint
import re
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from main.models import Category, Product, Store, History


class Command(BaseCommand):
    help = 'Collect all the categories present in the category table of the database.\
            It then collects the data according to these categories via the OFF API.'

    DICT_STORES = {
        r'auchan': "Auchan",
        r'(magasins?|hyper|super)[- ]u': "Magasins U",
        r'carrefour.*': "Carrefour",
        r'leclerc': "E-Leclerc",
        r'intermarche': "Intermarché",
        r'cora': "Cora",
        r'lidl': "Lidl",
        r'aldi': "Aldi",
        r'monoprix': "Monoprix",
        r'picard': "Picard",
        r'franprix': "Franprix",
        r'casino': "Casino",
        r'naturalia': "Naturalia"
    }

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
        categories = Category.objects.all()
        if not categories:
            print('The main_category table is empty, please feed it first to extract the categories.')
            return
        with open('main/management/commands/settings.json', 'r') as settings:
            self.data = json.load(settings)
        self.url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1"
        for category in categories:
            if category.name in self.data["categories_main"]:
                self.parameters = {'search_terms': category.name, 'page_size': self.data['page_size_main'],
                                   'page': page, 'fields': self.data['fields']}
            elif category.name in self.data["categories_sub"]:
                self.parameters = {'search_terms': category.name, 'page_size': self.data['page_size_sub'], 'page': page,
                                   'fields': self.data['fields']}
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
        dict = Command.DICT_STORES
        try:
            product = Product(code=raw_product['code'],
                              name=raw_product['product_name'].lower(),
                              nutriscore=raw_product['nutriscore_grade'],
                              description=raw_product['ingredients_text'],
                              url=raw_product['url'],
                              popularity=raw_product['unique_scans_n'])
            product.save()
            if "stores_tags" in raw_product:
                for store_element in raw_product['stores_tags']:
                    store = None
                    for regex in dict:
                        if bool(re.search(regex, store_element, flags=re.I)):
                            try:
                                store = Store(name=dict[regex])
                                store.save()
                            except DataError:
                                pass
                            except IntegrityError:
                                store = Store.objects.get(name=dict[regex])
                    if not store:
                        store = Store.objects.get(id=1)
                    product.store.add(store)
            product.category.add(category)
        except KeyError:
            pass
        except DataError:
            pass
        except IntegrityError:
            product = Product.objects.get(code=raw_product['code'])
            product.category.add(category)
