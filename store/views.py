from email import message
import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
import datetime
from .utils import cartData,guestOrder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return(render(request,'store/store.html',context))

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return(render(request,'store/cart.html',context))

@csrf_exempt
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return(render(request,'store/checkout.html',context))

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action =='add':
        orderitem.quantity=(orderitem.quantity+1)
    elif action =='remove':
        orderitem.quantity=(orderitem.quantity-1)

    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()

    return JsonResponse("item is added to the cart",safe=False)

def processItem(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        customer,order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete= True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address= data['shipping']['address'],
            city= data['shipping']['city'],
            zipcode= data['shipping']['zipcode'],
        )

    return JsonResponse("Payment completed successfully",safe=False)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid credentials")
            return redirect('/login/')

    data = cartData(request)
    cartItems = data['cartItems']
    context={'cartItems':cartItems}
    return(render(request,'store/login.html',context))


def createUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        print(request.POST)
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already taken! Try something different")
            return redirect('/login/')
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        messages.info(request,"User added successfully!")
        if(user is not None):
            pass
        customer = Customer.objects.create(user=user,name=username,email=email,password=password)
        customer.save()
        
    return redirect('/login/')

def logout(request):
    auth.logout(request)
    messages.info(request,"User is logged out")
    return redirect('/')