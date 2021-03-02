from django.db import models

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100)

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
    description = models.CharField(max_length=1000)
    url = models.CharField(max_length=200)
    store = models.ManyToManyField(Store)
    popularity = models.IntegerField()
    category = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return 'product: ' + self.name
