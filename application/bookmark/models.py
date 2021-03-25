from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from main.models import Product


# Create your models here.
class Substitution(models.Model):
    pass
    target_product = models.ForeignKey(Product, related_name="target_product", on_delete=CASCADE)
    source_product = models.ForeignKey(Product, related_name="source_product", on_delete=CASCADE)
    date_creation = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=CASCADE)

    class Meta:
        db_table = 'bookmark_substitution'
        constraints = [
            models.UniqueConstraint(fields=['target_product', 'source_product', 'user_id'], name='unique_substitution_user')
        ]

    def get_bookmarks_by_user(user_id):
        bookmarks = Substitution.objects.filter(user_id=user_id)
        return bookmarks

    def save_bookmark(source_id, target_id, user_id):
        bookmark_to_save = Substitution(source_product_id=source_id, target_product_id=target_id, user_id=user_id)
        bookmark_to_save.save()

    def delete_bookmark(source_id, target_id, user_id):
        bookmark_to_delete = Substitution.objects.get(source_product_id=source_id, target_product_id=target_id, user_id=user_id)
        bookmark_to_delete.delete()

    def specific_bookmark(source_id, target_id, user_id):
        try:
            substitution = Substitution.objects.get(source_product_id=source_id, target_product_id=target_id, user_id=user_id)
            if substitution:
                return True
        except ObjectDoesNotExist:
            return False
