import requests
from pprint import pprint
# from main.models import Product, Store, Category, History


def extract():
    terms = ['Coca Cola', 'saucisson', 'lait']
    url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1"
    for term in terms:
        parameters = {'search_terms': term, 'page-size': 10, 'page': 1, 'fields': "code,product_name,image_small_url"}
        r = requests.get(url=url, params=parameters)
        result = r.json()
        print(result)


extract()
