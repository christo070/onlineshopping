from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    city=models.CharField(max_length=20, null=True, blank=True)
    streetaddress=models.TextField()
    state=models.CharField(max_length=30, null=True, blank=True)
    country=models.CharField(max_length=30, null=True, blank=True)
    Zipcode=models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.id)


ACCOUNT_STATUS=(
    ('Active','Active'),
    ('Blocked','Blocked'),
    ('Banned','Banned'),
    ('Archived','Archived'),
    ('Unkown','Unkown'),
    ('Compromised','Compromised'),
)

class Account(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    status=models.CharField(max_length=50,choices=ACCOUNT_STATUS,default="Active")
    email=models.EmailField(max_length=250)
    phone=models.CharField(max_length=10)
    address=models.ForeignKey(Address,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.IntegerField
    available_count=models.IntegerField()
    category=models.ManyToManyField(ProductCategory)

    def __str__(self):
        return self.name



ORDER_STATUS=(
    ('Unshipped','Unshipped'),
    ('Pending','Pending'),
    ('Cancelled','Cancelled'),
    ('RefundApplicable','RefundApplicable'),
    ('Complete','Complete'),
    ('Shipped','Shipped'),
)

class Order(models.Model):
    orderNo=models.IntegerField()
    status=models.CharField(max_length=50,choices=ORDER_STATUS,default="Unshipped")
    orderDate=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.orderNo)

PAYMENT_STATUS=(
    ('Failed','Failed'),
    ('Unpaid','Unpaid'),
    ('Pending','Pending'),
    ('Completed','Completed'),
    ('Declined','Declined'),
    ('Settling','Settling'),
    ('Settled','Settled'),
    ('Cancelled','Cancelled'),
    ('Abandoned','Abandoned'),
    ('Refunded','Refunded'),
)


class Payment(models.Model):
    status=models.CharField(max_length=50,choices=PAYMENT_STATUS,default="Unshipped")
    amount=models.FloatField()
    order=models.ForeignKey(Order,on_delete=models.CASCADE,unique=True)

    def __str__(self):
        return str(self.id)