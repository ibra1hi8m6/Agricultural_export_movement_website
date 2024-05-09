from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    address=models.CharField(max_length=250, null=True)
    CommercialRegister=models.CharField(max_length=250, null=True)
    TaxCard=models.CharField(max_length=250, null=True)
    def __str__(self):
        return self.username




