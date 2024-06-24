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
    #model.cassade برای موقعی به کار می رود که میخوایم همه ارتباطات آن پاک شود
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
    #model.set_null برای موقعی که محصول پاک شود ولی فیلد های مرتبطش خالی گذاشته شود
    date_orderd=models.DateTimeField(auto_now_add=True)
    compelete=models.BooleanField(default=False,null=True,blank=False)
    #
    def __str__(self):
        return f'{str(self.customer)}({str(self.id)})({self.date_orderd})'
    #
    @property
    def get_cart_total(self):
        return sum(item.get_total for item in  self.orderitem_set.all())
    @property
    #این بخش برای مجموع سفارش ها است که با استفاده از پراپرتی میایم و تبدیل به ویژگی اوردر میکنیم 
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
class ShippingAddress(models.Model):
    customer= models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order= models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    date_aded=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address
class Slide(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE,blank=True,null=True)
    caption=models.TextField(max_length=400,null=True)
    def __str__(self):
        return self.product.name
class Scrool(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.product.name
            

# Create your models here.
