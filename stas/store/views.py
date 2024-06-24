from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from .models import *
from .forms import CreateUserForm
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
    context={'items':items,'len':len(items),'order':order,'cartItems':cartItems,'categories':categories}
    return render(request,'store/cart.html',context)
@login_required(login_url='login')
def checkout(request):
    categories=Category.objects.all()
    customer=request.user.customer
    order,created=Order.objects.get_or_create(customer=customer,compelete=False)
    if request.method=='GET':
        items=order.orderitem_set.all()
        context={'items':items,'len':len(items),'order':order,'categories':categories}
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
def login_page(request):
    if request.method== 'GET':
        categories=Category.objects.all()
        context={'categories':categories}
        return render(request,'store/login.html',context)
    elif request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
    try:
        try:
            user=User.objects.get(username=username)
        except:
            user=User.objects.get(email=username)
        if user is not None and user.check_password(password):
            login(request,user)
        if user.is_superuser:
            return redirect('panel')
        else:
            return redirect('store')
    except:
        return redirect('login')
def panel(request):
    if request.user.is_superuser:
        categories=Category.objects.all()
        datas=[]
        i=-1
        for sp_category in Category.objects.all():
            datas.append({})
            i+=1
            for sp_order_item in OrderItem.objects.all():
                if sp_order_item.product.category==sp_category:
                    if sp_order_item.date_aded.day in datas[i].keys():
                        datas[i][sp_order_item.date_aded.day]+=sp_order_item.quantity
                    else:
                        datas[i][sp_order_item.date_aded.day]=sp_order_item.quantity

        context={'categories':categories,'datas':datas}
        return render(request,'store/panel.html',context)   
    else:
        return HttpResponse(status=403)
def addproduct(request):
    if request.user.is_superuser:
        if request.method=='GET':
            categories=Category.objects.all()
            context={'categories':categories}
            return render(request,'store/addproduct.html',context)   
        if request.method=='POST':
            cat=Category.objects.get(name=request.POST.get('category'))
            img=request.FILES.get('image')
            Product.objects.create(name=request.POST.get('name'),category=cat,price=request.POST.get('price'),sugar=request.POST.get('sugar'),coffee=request.POST.get('coffee'),flour=request.POST.get('flour'),chocolate=request.POST.get('chocolate'),image=img)
            return redirect('show')
    else:
        return HttpResponse(status=403)
def show(request):
    if request.user.is_superuser:
        categories=Category.objects.all()
        products=Product.objects.all()
        context={'categories':categories,'products':products}
        return render(request,'store/show.html',context)   
    else:
        return HttpResponse(status=403)
def storage(request):
    if request.user.is_superuser:
        if request.method=='GET':
            categories=Category.objects.all()
            storages=Storage.objects.all()
            context={'categories':categories,'storages':storages}
            return render(request,'store/storage.html',context) 
        if request.method=='POST':
            sugar=Storage.objects.get(name='sugar')
            sugar.amount=request.POST.get('sugar')
            sugar.save()
            coffee=Storage.objects.get(name='coffee')
            coffee.amount=request.POST.get('coffee')
            coffee.save()
            flour=Storage.objects.get(name='flour')
            flour.amount=request.POST.get('flour')
            flour.save()
            chocolate=Storage.objects.get(name='chocolate')
            chocolate.amount=request.POST.get('chocolate')
            chocolate.save()
            return redirect('storage')
    else:
        return HttpResponse(status=403)
def history(request):
    categories=Category.objects.all()
    cusromer=Customer.objects.filter(name=request.user.username).first()
    orders=Order.objects.filter(customer=cusromer,compelete=True)
    context={'categories':categories,'orders':orders}
    return render(request,'store/history.html',context)   
def logout_page(request):
    logout(request)
    return redirect('store')
def signup(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form=CreateUserForm()
        if request.method=="POST":
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                new_user_name=form['username'].value()
                new_user_email=form['email'].value()
                new_user_object=User.objects.filter(username=form['username'].value()).first()
                Customer.objects.create(user=new_user_object,email=new_user_email,name=new_user_name)
                return redirect('login')
        categories=Category.objects.all()
        context={'categories':categories,'form':form}
        return render(request,'store/signup.html',context)
@login_required(login_url='login')
def profile(request):
    categories=Category.objects.all()
    cusromer=Customer.objects.filter(name=request.user.username).first()
    context={'categories':categories,'customer':cusromer}
    return render(request,'store/profile.html',context)
def products(request,id):
    id=int(id)
    category_products=[]
    categories=Category.objects.all()
    if id<=len(categories) and id>0:
        for product in Product.objects.all():
            if int(product.category.id)==id:
                category_name=product.category
                category_products.append(product)
        context={'category_products':category_products,'categories':categories,'id':id,'category_name':category_name}
        return render(request,'store/products.html',context)
    else:
        return redirect('store')
def updateItem(request):
    data=json.loads(request.body)
    ProductID=data['ProductId']
    action=data['action']
    customer=request.user.customer
    product=Product.objects.get(id=ProductID)
    order,created=Order.objects.get_or_create(customer=customer,compelete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    st_sugar=Storage.objects.get(name='sugar')
    st_coffee=Storage.objects.get(name='coffee')
    st_flour=Storage.objects.get(name='flour')
    st_chocolate=Storage.objects.get(name='chocolate')
    if action=='add':
        if st_sugar.amount-product.sugar>=0 and st_coffee.amount-product.coffee>=0 and st_flour.amount-product.flour>=0 and st_chocolate.amount-product.chocolate>=0:
            orderItem.quantity=(orderItem.quantity+1)
            st_sugar.amount=st_sugar.amount-product.sugar
            st_sugar.save()
            st_coffee.amount=st_coffee.amount-product.coffee
            st_coffee.save()
            st_flour.amount=st_flour.amount-product.flour
            st_flour.save()
            st_chocolate.amount=st_chocolate.amount-product.chocolate
            st_chocolate.save()
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
        st_sugar.amount=st_sugar.amount+product.sugar
        st_sugar.save()
        st_coffee.amount=st_coffee.amount+product.coffee
        st_coffee.save()
        st_flour.amount=st_flour.amount+product.flour
        st_flour.save()
        st_chocolate.amount=st_chocolate.amount+product.chocolate
        st_chocolate.save()
    orderItem.save()
    if orderItem.quantity<=0:orderItem.delete()
    return JsonResponse("item added",safe=False)
