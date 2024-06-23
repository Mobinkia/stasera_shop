from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *







def store(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,compelete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
        cartItems=order['get_cart_items']
    products=Product.objects.all()
    categories=Category.objects.all()
    slides=Slide.objects.all()
    scrool=Scrool.objects.all()
    context={'products':products,'cartItems':cartItems,'categories':categories,'slides':slides,'scrool':scrool}
    return render(request,'store/store.html',context)
@login_required(login_url='login')


# Create your views here.
