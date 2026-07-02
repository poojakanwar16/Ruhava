from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15 , unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    address = models.TextField(null=True ,blank=True)
    login_as =  models.CharField(
    max_length=20,
    choices=[
        ("customer", "Customer"),
        ("shopkeeper", "Shopkeeper"),
    ],
    default="customer"
)
    
    def __str__(self):
        return self.user.username

class feedback(models.Model):
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    msg=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username