from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category/")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name    
    class Meta:
        verbose_name_plural = "Categories"    #django by default convert into plural so it was looking categorys which is wrong

class Product(models.Model):
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    ]

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    colour=models.CharField(default="not added yet")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    stock = models.PositiveIntegerField(default=1)
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),)
    sizes = MultiSelectField(
        choices=SIZE_CHOICES,
        max_choices=4,
        max_length=10,
        blank=True,
        default=""
    )
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return str(self.product) 
    

