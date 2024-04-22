from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def detail(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    context= {'products': products,'items': items, 'order': order, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/detail.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    return render(request, 'app/search.html', {"searched": searched, "keys": keys})

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        user_not_login = "show"
        user_login = "hidden"
    products = Product.objects.all()
    context= {'products': products, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        user_not_login = "show"
        user_login = "hidden"
    context= {'items': items, 'order': order, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        user_not_login = "show"
        user_login = "hidden"
    context= {'items': items, 'order': order, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order,created = Order.objects.get_or_create(customer = customer,complete = False)
    orderItem,created = OrderItem.objects.get_or_create(order = order,product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('added', safe=False)

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            customer = Customer.objects.create(user=user, name=username, email=user.email)

            order = Order.objects.create(customer=customer)

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You have registered successfully.")
            return redirect('home')
        else:
            messages.error(request, "Whoops! There was a problem registering. Please try again.")
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request, 'app/register.html', {'form': form})

from .forms import LoginForm

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "There was an error, please try again...")
            return redirect('login')

    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out. Thanks for stopping by.")
    return redirect('login')