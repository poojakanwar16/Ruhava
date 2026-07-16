from django.db import models
from django.conf import settings
from django.contrib.auth.models import User 
import random
from shopkeeper.models import Product
from datetime import timedelta
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out For Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    # Customer details
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # Order information
    total_amount = models.DecimalField( max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items" )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    shopkeeper = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopkeeper_orders"
    )

    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=10)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} ({self.order.id})"
        