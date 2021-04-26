# from django.db.models.aggregates import Max
# from django.db.models.deletion import CASCADE
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
    salt = models.CharField(max_length=10)
    sugars = models.CharField(max_length=10)
    saturated = models.CharField(max_length=10)
    fat = models.CharField(max_length=10)
    image_url = models.CharField(max_length=100)
    small_image_url = models.CharField(max_length=100)

    def __str__(self) -> str:
        return 'product: ' + self.name

    def retrieve_prod_with_pk(pk):
        """
        retrieves a product with its primary key
        """
        product = Product.objects.get(pk=pk)
        return product

    def retrieve_product(request):
        """
        Function used to retrieve the product matching the best with the user request.
        """
        scores = {}
        user_request = request.replace('-', ' ')
        nb_words_request = len(user_request.split(' '))
        products = Product.objects.annotate(search=SearchVector('name')).filter(search=user_request)
        if products:
            for product in products:
                score, score_2 = 0, 0
                string_product = product.name.replace('-', ' ').lower().split(' ')
                for word in string_product:
                    score += 1 if word in user_request.lower() else score
                score_final_1 = round((score/nb_words_request) * 100)
                for word in user_request.split(' '):
                    score_2 += 1 if word.lower() in string_product else score_2
                score_final_2 = round((score_2/len(string_product)) * 100)
                score_final_1 = 100 if score_final_1 > 100 else score_final_1
                score_final_2 = 100 if score_final_2 > 100 else score_final_2
                score_final = (score_final_1 + score_final_2) / 2
                if score_final == 100:
                    category = product.category.all()
                    return product, category
                scores[score_final] = product.code
            if scores:
                maxi = 0
                for key in scores:
                    maxi = key if key > maxi else maxi
                winner = Product.objects.get(code=scores[maxi])
                category = product.category.all()
                return winner, category
        else:
            return None, None

    def looking_for_suggestion(winner_code, target_nutriscore, categories, j):
        """
        Function looking for the suggestions in the chosen category.
        """
        results = Product.objects.filter(category=categories[j].id, nutriscore=target_nutriscore)
        nb = [element for element in results]
        nb.remove(winner_code) if winner_code in nb else None
        return nb

    def generate_suggestions(categories, winner):
        """
        Function formating and generating the chosen suggestions.
        """
        nutri = ['a', 'b', 'c', 'd', 'e']
        pre_suggestions = []
        i = 0
        j = 1
        while len(pre_suggestions) < 6:
            results = Product.looking_for_suggestion(winner.code, nutri[0 + i], categories, j)
            if winner.nutriscore == nutri[0 + i]:
                if i == 0 and j == 0:
                    return 0
                if pre_suggestions != []:
                    suggestions = [Product.objects.get(code=element.code) for element in pre_suggestions]
                    if j == 1:
                        j, i = 0, 0
                    else:
                        return suggestions
                elif pre_suggestions == [] and j == 0:
                    return 0
                elif pre_suggestions == [] and j == 1:
                    j, i = 0, 0
            else:
                for element in results:
                    pre_suggestions.append(element)
                i += 1
        suggestions = [Product.objects.get(code=element.code) for element in pre_suggestions[:6]]
        return suggestions


class History(models.Model):
    page_number = models.IntegerField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
