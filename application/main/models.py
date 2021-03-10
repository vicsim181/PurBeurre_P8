from pprint import pprint
from django.db import models
from django.utils import timezone
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

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
        vector = SearchVector('name')
        query = SearchQuery(request)
        winner = Product.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')[0]
        category = Category.objects.filter(product__id=winner.id)
        if winner:
            return winner, category

    def looking_for_suggestion(winner_code, target_nutriscore, categories, j):
        """
        Function looking for the suggestions in the chosen category.
        """
        results = Product.objects.filter(category=categories[j].id, nutriscore=target_nutriscore)
        nb = []
        for element in results:
            nb.append(element.code)
        if winner_code in nb:
            nb.remove(winner_code)
        print('NB LOOKING FOR: ' + str(nb))
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
            if winner.nutriscore == nutri[0 + i]:
                j, i = 0, 0
            results = Product.looking_for_suggestion(winner.code, nutri[0 + i], categories, j)
            for element in results:
                pre_suggestions.append(element)
            i += 1
        # str_stores = []
        # for i in range(0, 5):
        #     suggestions += Model.SES.query(Product).filter(Product.Id == suggestions[i])
        #     id_stores = Model.SES.query(StoreProduct.id_store).filter(StoreProduct.id_product == suggestions[i])
        #     str_stores.append(Model.format_stores(id_stores))
        # for element in pre_suggestions[-6:]:
        suggestions = [Product.objects.get(code=element) for element in pre_suggestions[-6:]]
        return suggestions  # str_stores


class History(models.Model):
    page_number = models.IntegerField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
