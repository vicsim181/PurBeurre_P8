import requests
import pprint
# from main.models import Product, Store, Category, History


def extract():
    terms = ['soda cola', 'saucisson sec', 'fromage', 'camembert']
    url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1"
    for term in terms:
        parameters = {'search_terms': term, 'page-size': 50, 'page': 1,
                      'fields': "code,product_name,nutriscore_grade,url,stores_tags,unique_scans_n,\
                                 image_url,image_small_url"}
        r = requests.get(url=url, params=parameters)
        result = r.json()
        pprint.pprint(result)


extract()
