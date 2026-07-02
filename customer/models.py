from django.db import models
from django.conf import settings
from shopkeeper.models import Product,ProductImage
from django.contrib.auth.models import User
     
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('shopkeeper.Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
