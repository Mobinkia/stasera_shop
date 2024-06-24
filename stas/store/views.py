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

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,compelete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
        cartItems=order['get_cart_items']
    categories=Category.objects.all()
    context={'items':items,'order':order,'cartItems':cartItems,'categories':categories}
    return render(request,'store/cart.html',context)
@login_required(login_url='login')

def checkout(request):
    categories=Category.objects.all()
    customer=request.user.customer
    order,created=Order.objects.get_or_create(customer=customer,compelete=False)
    if request.method=='GET':
        items=order.orderitem_set.all()
        context={'items':items,'order':order,'categories':categories}
        return render(request,'store/checkout.html',context)
    elif request.method=='POST':
        address=request.POST.get('address')
        state=request.POST.get('state')
        zipcode=request.POST.get('zipcode')
        city=request.POST.get('city')
        ShippingAddress.objects.create(address=address,state=state,zipcode=zipcode,city=city,customer=customer,order=order)
        order.compelete=True
        order.save()
        Order.objects.create(customer=customer)
        return redirect('store')


# Create your views here.
