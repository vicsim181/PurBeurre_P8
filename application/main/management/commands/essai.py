from pprint import pprint
from main.models import Product
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'essai de retrouver produit'

    def handle(self, *args, **options):
        # product = Product.objects.get(id=1)
        scores = {}
        request = 'magnum glace batonnet blanc chocolat'
        nb_words_request = len(request.split(' '))
        products = Product.objects.filter(name__icontains=request)
        print(products)
        for product in products:
            score = 0
            string_product = product.name.split(' ')
            for word in string_product:
                print('word: ' + word + 'request: ' + request)
                if word.lower() in request:
                    score += 1
            score_final = round((score/nb_words_request)*100)
            scores[score_final] = product.code
        print(scores)
        if scores:
            max = 0
            for key in scores:
                if key > max:
                    max = key
            winner = Product.objects.get(code=scores[max])
            return winner.name + ' ' + winner.code
        # return product.code
        # print(product.code)
