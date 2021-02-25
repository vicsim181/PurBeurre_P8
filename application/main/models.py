from django.db import models

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Product(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    description = models.CharField(max_length=200)
    url = models.URLField
    store = models.ManyToManyField(Store)
    category = models.ManyToManyField(Category)
