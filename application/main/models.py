import pprint
from django.db.models.deletion import CASCADE
from django.db import models
from django.utils import timezone
from django.contrib.postgres.search import SearchVector

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return 'store: ' + self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return 'category: ' + self.name


class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    description = models.TextField()
    url = models.CharField(max_length=200)
    store = models.ManyToManyField(Store)
    popularity = models.IntegerField()
    category = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return 'product: ' + self.name

    def retrieve_product(request):
        """
        Function used to retrieve the product matching the best with the user request.
        """
        scores = {}
        user_request = request.replace('-', ' ')
        nb_words_request = len(user_request.split(' '))
        # print('NB WORD REQUEST: ' + str(nb_words_request))
        products = Product.objects.annotate(search=SearchVector('name')).filter(search=user_request)
        # print(products)
        if products:
            for product in products:
                score = 0
                string_product = product.name.replace('-', ' ').split(' ')
                for word in string_product:
                    if word.lower() in user_request.lower():
                        score += 1
                score_final = round((score/nb_words_request) * 100)
                # print('SCORE 1: ' + str(score_final))
                if score_final >= 100:
                    score_final_2 = round((score/len(string_product)) * 100)
                    # print('SCORE 2: ' + str(score_final_2))
                    score_final = (100 + score_final_2) / 2
                # print('product: ' + str(string_product) + '   request: ' + request +
                    #   ' nb_words_request ' + str(nb_words_request))
                # print(score_final)
                if score_final == 100:
                    scores[score_final] = product.code
                    winner = Product.objects.get(code=product.code)
                    category = Category.objects.filter(product__id=winner.id)
                    return winner, category
                scores[score_final] = product.code
            # print(scores)
            if scores:
                max = 0
                for key in scores:
                    if key > max:
                        max = key
                winner = Product.objects.get(code=scores[max])
                category = Category.objects.filter(product__id=winner.id)
                return winner, category
        else:
            return None, None

    def looking_for_suggestion(winner_code, target_nutriscore, categories, j):
        """
        Function looking for the suggestions in the chosen category.
        """
        # print('BEGIN LOOKING FOR SUGGESTION')
        results = Product.objects.filter(category=categories[j].id, nutriscore=target_nutriscore)
        nb = [element for element in results]
        nb.remove(winner_code) if winner_code in nb else None
        return nb

    def generate_suggestions(categories, winner):
        """
        Function formating and generating the chosen suggestions.
        """
        # print("BEGIN GENERATE_SUGGESTION")
        nutri = ['a', 'b', 'c', 'd', 'e']
        pre_suggestions = []
        i = 0
        len_cat = len(categories)
        if len_cat == 1:
            j = 0
        elif len_cat == 2:
            j = 1
        while len(pre_suggestions) < 6:
            # print('WINNER NUTRI: ' + winner.nutriscore + '    NUTRI TARGET: ' + nutri[0+i])
            if winner.nutriscore == nutri[0 + i]:
                if pre_suggestions != []:
                    if len(pre_suggestions) < 6:
                        suggestions = [Product.objects.get(code=element.code) for element in pre_suggestions[:len(pre_suggestions)]]
                    else:
                        suggestions = [Product.objects.get(code=element.code) for element in pre_suggestions[:6]]
                        return suggestions
                if j == 0 and j == 0:
                    return 0
                else:
                    j, i = 0, 0
            # print('I J: ' + str(i) + ' ' + str(j))
            results = Product.looking_for_suggestion(winner.code, nutri[0 + i], categories, j)
            for element in results:
                pre_suggestions.append(element)
            i += 1
        if pre_suggestions != []:
            # print(pre_suggestions)
            suggestions = [Product.objects.get(code=element.code) for element in pre_suggestions[:6]]
            return suggestions
        else:
            return 0


class History(models.Model):
    page_number = models.IntegerField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
