from audioop import add
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
import razorpay
from OnlineBazaar.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET
import time
from math import ceil
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
		addressline1 = request.POST['addressline1']
		street=request.POST['street']
		city=request.POST['city']
		pincode=request.POST['pincode']
		country=request.POST['country']
		state=request.POST['state']

		try:
			account = request.user.account
			myaddress=Address(AddressLine1=addressline1,city=city,street=street,state=state,country=country,Zipcode=pincode,account=account)
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


client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))
def rz_payment_integration(request):

	week_limit = 604800
	invoice_expiry = ceil(time.time()) + week_limit

	account = request.user.account
	firstname = account.firstname
	lastname = account.lastname
	phone = account.phone
	email = account.email
	address=account.address_set.all()[0]
	s_cart, created = S_cart.objects.get_or_create(account = account)
	cartitems = s_cart.cartitem_set.all()
	# print(cartitems)

	cart_items = list()
	for j in cartitems:
		cart_items.append({'name':j.product.name,'description':'','amount':j.product.price*100,'quantity':j.quantity,'currency':'INR'})
	
	
	obj = client.invoice.create({
	"type": "invoice",
	"description": "OnlineBazaar",
	"partial_payment": 0,
	"customer": {
		"name": firstname+" "+lastname,
		"contact": phone,
		"email": email,
		"billing_address": {
		"line1": address.AddressLine1,
		"line2": address.street,
		"zipcode": address.Zipcode,
		"city": address.city,
		"state": address.state,
		"country": "in"
		},
		"shipping_address": {
		"line1": address.AddressLine1,
		"line2": address.street,
		"zipcode": address.Zipcode,
		"city": address.city,
		"state": address.state,
		"country": "in"
		}
	},
	"line_items":cart_items,
	"sms_notify": 0,
	"email_notify": 1,
	"currency": "INR",
	"expire_by": invoice_expiry
	})

	context = {'order_id':obj['order_id'],'amount':obj['amount'],'username':firstname+" "+lastname,'rz_key':RAZORPAY_API_KEY,'address':address,'email':email,'contact':phone}
	return render(request,'store/payment.html',context)
