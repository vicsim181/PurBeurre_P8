from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100)


class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    hash_password = models.CharField(max_length=90)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


class CategoryParents(models.Model):
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutriscore = models.CharField(max_length=1)
    description = models.CharField(max_length=200)
    url = models.URLField
    store = models.ManyToManyField(Store, null=True)


class Favorite(models.Model):
    id_replaced_product = models.ForeignKey(Product, on_delete=CASCADE)
    id_replacing_product = models.ForeignKey(Product, on_delete=CASCADE)
    date_creation = models.DateTimeField(default=timezone.now())
    user_id = models.ForeignKey(User, on_delete=CASCADE)
