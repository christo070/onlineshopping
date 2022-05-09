import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
# from requests import request
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from .models import Product
from django.http import JsonResponse
# Create your views here.

def	checksignedin(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			return JsonResponse({'signed in':True})
		else:
			return JsonResponse({'signed in':False})


def home(request):
	if request.user.is_authenticated:
		account = request.user.account
		s_cart, created = S_cart.objects.get_or_create(account = account)
		cartitems = s_cart.cartitem_set.all()
		totitems = s_cart.get_cart_items

	else:
		cartitems = []
		s_cart = {'get_cart_total':0, 'get_cart_items':0}
		totitems = s_cart['get_cart_items']

	products = Product.objects.all()
	categories = ProductCategory.objects.all()
	context = {'products': products, 'categories': categories ,'totitems':totitems}
	return render(request, 'store/home.html', context)



def cart(request):
	if request.user.is_authenticated:
		account = request.user.account
		s_cart, created = S_cart.objects.get_or_create(account = account)
		cartitems = s_cart.cartitem_set.all()
		totitems = s_cart.get_cart_items

	else:
		cartitems = []
		s_cart = {'get_cart_total':0, 'get_cart_items':0}
		totitems = s_cart['get_cart_items']

	context = {'cartitems':cartitems, 's_cart':s_cart ,'totitems':totitems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.method=='GET':
		
		if not request.user.is_authenticated:
			return HttpResponse('you are not login')
			# cartitems = []
			# s_cart = {'get_cart_total':0, 'get_cart_items':0}
			# address=NULL
		
		account = request.user.account
		s_cart, created = S_cart.objects.get_or_create(account = account)
		cartitems = s_cart.cartitem_set.all()
		address=account.address_set.all()
		context = {'cartitems':cartitems, 's_cart':s_cart,'address':address}
		return render(request, 'store/checkout.html', context)


	if request.method=='POST':
		if not request.user.is_authenticated:
			return HttpResponse('you are not login')

		# for i in request.POST.keys():
		# 	print(i,request.POST[i])
		city=request.POST['city']
		streetaddress=request.POST['streetaddress']
		country=request.POST['country']
		state=request.POST['state']
		pincode=request.POST['pincode']

		try:
			account = request.user.account
			myaddress=Address(city=city,streetaddress=streetaddress,state=state,country=country,Zipcode=pincode,account=account)
			myaddress.save()
			# now payment process will be processed
		except:
			messages.success(request,"Address not deliverable")
		account = request.user.account
		s_cart, created = S_cart.objects.get_or_create(account = account)
		cartitems = s_cart.cartitem_set.all()
		address=account.address_set.all()
		print(address)
		context = {'cartitems':cartitems, 's_cart':s_cart,'address':address}
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
		password1=request.POST['password']
		password2=request.POST['password1']
		
		try:
			myuser=User.objects.create_user(username=username,email=email,password=password1)
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

		user=authenticate(request,username=username,password=password)
		if user is not None:
			print(user)
			print("hello world")
			login(request,user)
			return redirect('/')
			
		else:
			messages.success(request,"Username or password Incorrect")
			return render(request,'store/sign-in.html',context)


def signout(request):
	if request.method == "GET":
		if request.user.is_authenticated:
			logout(request)
			return render(request,'store/home.html')
		

def productdetail(request,id="#"):
	if request.method=="GET":
		if id=='#':
			return HttpResponse('No product is chosen ')
		product=Product.objects.get(id=id)
		
		return render(request,'store/product.html',{'product':product})



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	account = request.user.account
	product = Product.objects.get(id=productId)
	s_cart, created = S_cart.objects.get_or_create(account=account)

	cartitem, created = CartItem.objects.get_or_create(scart=s_cart, product=product)

	if action == 'add':
		cartitem.quantity = (cartitem.quantity + 1)
	elif action == 'remove':
		cartitem.quantity = (cartitem.quantity - 1)

	cartitem.save()

	if action == 'delete':
		cartitem.delete()

	if cartitem.quantity <= 0:
		cartitem.delete()

	return JsonResponse('Item was added', safe=False)

