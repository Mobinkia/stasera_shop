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
class Order(models.Model):
    customer= models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_orderd=models.DateTimeField(auto_now_add=True)
    compelete=models.BooleanField(default=False,null=True,blank=False)
    def __str__(self):
        return f'{str(self.customer)}({str(self.id)})({self.date_orderd})'
    def compeleted(self):
        self.compelete=True
    @property
    def get_cart_total(self):
        return sum(item.get_total for item in  self.orderitem_set.all())
    @property
    def get_cart_items(self):
        return sum(item.quantity for item in  self.orderitem_set.all())
class OrderItem(models.Model):
    product= models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order= models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,blank=True,null=True)
    date_aded=models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        return self.product.price*self.quantity        

# Create your models here.



# Create your models here.
