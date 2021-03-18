from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from main.models import Product
from authentication.models import User


# Create your models here.
class Substitution(models.Model):
    target_product = models.ForeignKey(Product, related_name="target_product", on_delete=CASCADE)
    source_product = models.ForeignKey(Product, related_name="source_product", on_delete=CASCADE)
    date_creation = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=CASCADE)
