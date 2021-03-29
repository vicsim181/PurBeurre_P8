from datetime import datetime
from django.db.utils import DataError
import requests
import json
import urllib.request as urlreq
from urllib.error import HTTPError, URLError
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
        # categories = Category.objects.all()
        # if not categories:
            # print('The main_category table is empty, please feed it first to extract the categories.')
            # return
        with open('main/management/commands/settings.json', 'r') as settings:
            self.data = json.load(settings)
        categories_settings = self.data['categories']
        # cat_set_values = categories_settings.values()
        # print(cat_set_values)
        self.url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1"
        for main_category in categories_settings:
            for sub_category in categories_settings[main_category]:
                # print(sub_category)
                self.parameters = {'search_terms': sub_category, 'page_size': self.data['page_size'],
                                   'page': page, 'fields': self.data['fields']}
                self.extract_data(main_category, sub_category)
            # print(main_category)
            # self.parameters = {'search_terms': main_category, 'page_size': self.data['page_size_main'], 'page': page,
            #                    'fields': self.data['fields']}
            # self.extract_data(main_category)
        history = History(page_number=page)
        history.save()
        print('DONE! Database fed on ' + str(datetime.now()) + ' with page ' + str(page))

    def extract_data(self, main_category_name, sub_category_name):
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
            self.treat_data(raw_product, main_category_name, sub_category_name)

    def treat_data(self, raw_product, main_category_name, sub_category_name):
        """
        Function that inserts a new product in the database if it's not already in.
        It also adds links between products and their categories and stores.
        """
        dict = Command.DICT_STORES
        try:
            main_category = Category.objects.get(name=main_category_name)
            sub_category = Category.objects.get(name=sub_category_name)
            product = Product(code=raw_product['code'],
                              name=raw_product['product_name'].lower(),
                              nutriscore=raw_product['nutriscore_grade'],
                              description=raw_product['ingredients_text'],
                              url=raw_product['url'],
                              popularity=raw_product['unique_scans_n'],
                              salt=raw_product['salt_100g'],
                              sugars=raw_product['sugars_100g'],
                              saturated=raw_product['saturated-fat_100g'],
                              fat=raw_product['fat_100g'])

            product.save()
            product.category.add(main_category)
            product.category.add(sub_category)
            try:
                imgurl = raw_product['image_url']
                urlreq.urlretrieve(imgurl, "static/img/products/" + raw_product['code'] + '.jpg')
                small_imgurl = raw_product['image_small_url']
                urlreq.urlretrieve(small_imgurl, "static/img/products_small/" + raw_product['code'] + '.jpg')
            except HTTPError:
                pass
            except URLError:
                pass
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
            # prod_categories = product.category.all()
            # if len(prod_categories) < 2:
                # product.category.add(category)
        except KeyError:
            pass
        except DataError:
            pass
        except IntegrityError:
            pass
            # product = Product.objects.get(code=raw_product['code'])
            # prod_categories = product.category.all()
            # if len(prod_categories) < 2:
            #     product.category.add(category)
