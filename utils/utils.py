import requests
import json
import pprint
import re


def stores():
    url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1"
    parameters = {'search_terms': 'fromage', 'page_size': 1000, 'fields': 'stores_tags'}
    r = requests.get(url=url, params=parameters)
    result = r.json()
    raw_stores = result['products']
    for raw_store in raw_stores:
        if "stores_tags" in raw_store:
            store_treatment(raw_store['stores_tags'])


def store_treatment(raw_store):
    for store in raw_store:
        regex_list = list(dic_stores.keys())
        for regex in regex_list:
            if bool(re.search(regex, store, flags=re.I)):
                print(store + ' --> ' + dic_stores[regex])
                # return store + ' ' + dic_stores[store]


dic_stores = {
    r"auchan": "Auchan",
    r"(magasins?|hyper|super)[- ]u": "Magasins U",
    r"carrefour.*": "Carrefour",
    r"leclerc": "E-Leclerc",
    r"intermarche": "Intermarché",
    r"cora": "Cora",
    r"lidl": "Lidl",
    r"aldi": "Aldi",
    r"monoprix": "Monoprix",
    r"picard": "Picard",
    r"franprix": "Franprix",
    r"casino": "Casino"
}

stores()
#   r"((magasins*[- ])|(hyper[- ])|(super[- ]))u": "Magasins U",
