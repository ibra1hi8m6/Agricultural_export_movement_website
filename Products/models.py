from django.db import models
from django.contrib.auth import get_user_model  # Import the get_user_model function


# Create your models here.
class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    mainImage = models.ImageField(upload_to='photos/', null=True, blank=True)
    def __str__(self):
        return self.categoryName

class ProductsName(models.Model):
    nameOfProducts=models.CharField(max_length=100)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE , null=True)
    def __str__(self):
        return self.nameOfProducts





class Product(models.Model):
    productName = models.CharField(max_length=255)
    mainImage = models.FileField(upload_to='photos/', null=True, blank=True)
    price = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True ,related_name='product_set')
    quantity=models.IntegerField(null=True)
    def __str__(self):
        return self.productName







