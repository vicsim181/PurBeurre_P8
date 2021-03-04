from django.db import models
from django.utils import timezone

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
    category = models.ManyToManyField(Category, on_delete=CASCADE)

    def __str__(self) -> str:
        return 'product: ' + self.name


class History(models.Model):
    page_number = models.IntegerField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
