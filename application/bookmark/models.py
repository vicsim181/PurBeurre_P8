from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.conf import settings
from main.models import Product


# Create your models here.
class Substitution(models.Model):
    pass
    target_product = models.ForeignKey(Product, related_name="target_product", on_delete=CASCADE)
    source_product = models.ForeignKey(Product, related_name="source_product", on_delete=CASCADE)
    date_creation = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=CASCADE)
