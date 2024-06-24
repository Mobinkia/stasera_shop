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

def login_page(request):
    if request.method== 'GET':
        categories=Category.objects.all()
        context={'categories':categories}
        return render(request,'store/login.html',context)
    elif request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
    try:
        user=User.objects.get(username=username)
        if user is not None and user.check_password(password):
            login(request,user)
        if user.is_superuser:
            return redirect('panel')
        else:
            return redirect('store')
    except:
        return redirect('login')

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

def logout_page(request):
    logout(request)
    return redirect('store')

def updateItem(request):
    data=json.loads(request.body)
    ProductID=data['ProductId']
    action=data['action']
    print("-------------")
    print(ProductID)
    print(action)
    customer=request.user.customer
    product=Product.objects.get(id=ProductID)
    order,created=Order.objects.get_or_create(customer=customer,compelete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity<=0:orderItem.delete()
    return JsonResponse("item added",safe=False)

def history(request):
    categories=Category.objects.all()
    cusromer=Customer.objects.filter(name=request.user.username).first()
    orders=Order.objects.filter(customer=cusromer,compelete=True)
    context={'categories':categories,'orders':orders}
    return render(request,'store/history.html',context) 

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
            if int(product.category.id)==id:category_products.append(product)
        context={'category_products':category_products,'categories':categories,'id':id}
        return render(request,'store/products.html',context)
    else:
        return redirect('store')

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


# Create your views here.
