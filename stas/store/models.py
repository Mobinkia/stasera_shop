from django.db import models
from django.contrib.auth.models import User
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
class Category(models.Model):
    name=models.CharField(max_length=200,null=True)
    icon=models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    image=models.ImageField(null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name
    @property
    def imgaeURL(self):
        try:
            url=self.image.url
        except:
            url=""
            return url

# Create your models here.
