from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Product
# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'store/home.html', context)


def cart(request):
	if request.user.is_authenticated:
		account = request.user.account
		s_cart, created = S_cart.objects.get_or_create(account = account)
		cartitems = s_cart.cartitem_set.all()

	else:
		cartitems = []
		s_cart = {'get_cart_total':0, 'get_cart_items':0}

	context = {'cartitems':cartitems, 's_cart':s_cart}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		account = request.user.account
		s_cart, created = S_cart.objects.get_or_create(account = account)
		cartitems = s_cart.cartitem_set.all()

	else:
		cartitems = []
		s_cart = {'get_cart_total':0, 'get_cart_items':0}
	context = {'cartitems':cartitems, 's_cart':s_cart}
	return render(request, 'store/checkout.html', context)

def signup(request):
	context={}
	if request.method=="GET":
		return render(request,'store/sign-up.html',context)
	if request.method=="POST":
		for i in request.POST.keys():
			print(i, request.POST[i])
		username=request.POST['username']
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		phone=request.POST['phone']
		email=request.POST['email']
		password=request.POST['password']
		password1=request.POST['password1']
		
		try:
			myuser=User.objects.create(username=username,email=email,password=password)
			myuser.save()
		except:
			messages.success(request,"Username already taken")
		else:
			accn=Account(user=myuser,lastname=lastname,firstname=firstname,email=email,phone=phone)
			accn.save()
			messages.success(request,"Your account is successfully created . Login in to your account")

		return render(request,'store/sign-up.html',context)

def signin(request):
	context={}
	if request.method=="GET":
		return render(request,'store/sign-in.html',context)
	if request.method=="POST":
		for i in request.POST.keys():
			print(i, request.POST[i])
		username=request.POST['username']
		password=request.POST['password']

		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return render(request,'store/home.html',context)
		else:
			messages.success(request,"Username or password Incorrect")
			return render(request,'store/sign-in.html',context)

def productdetail(request,id="#"):
	if request.method=="GET":
		if id=='#':
			return HttpResponse('No product is chosen ')
		product=Product.objects.all()
		# product=Product.objects.filter(id=id)
		print(product)
		return render(request,'store/productdetail.html',{'products':product})

