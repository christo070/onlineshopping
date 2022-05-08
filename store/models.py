from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Address(models.Model):
    city = models.CharField(max_length=20, null=True, blank=True)
    streetaddress = models.TextField()
    state = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    Zipcode = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.city)


ACCOUNT_STATUS = (
    ('Active', 'Active'),
    ('Blocked', 'Blocked'),
    ('Banned', 'Banned'),
    ('Archived', 'Archived'),
    ('Unkown', 'Unkown'),
    ('Compromised', 'Compromised'),
)


class Account(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    status=models.CharField(max_length=50,choices=ACCOUNT_STATUS,default="Active")
    email=models.EmailField(max_length=250, null=True, blank=True)
    phone=models.CharField(max_length=10, null=True, blank=True)
    address=models.ForeignKey(Address,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.firstname


class ProductCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    price = models.FloatField(null=True, blank=False)
    available_count = models.IntegerField()
    category = models.ManyToManyField(ProductCategory)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class S_cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    cart_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.cart_id)

    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()        
        total = sum([item.quantity for item in cartitems])
        return total

    @property
    def get_cart_total(self):
        cartitems = self.cartitem_set.all()        
        total = sum([item.get_total for item in cartitems])
        return total

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    scart = models.ForeignKey(S_cart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class S_cart(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    cart_no = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


    @property
    def get_cart_items(self):
        orderitems = self.cartitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    scart = models.ForeignKey(S_cart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


ORDER_STATUS = (
    ('Unshipped', 'Unshipped'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
    ('RefundApplicable', 'RefundApplicable'),
    ('Complete', 'Complete'),
    ('Shipped', 'Shipped'),
)


class Order(models.Model):
    orderNo = models.IntegerField()
    status = models.CharField(
        max_length=50, choices=ORDER_STATUS, default="Unshipped")
    orderDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.orderNo)


PAYMENT_STATUS = (
    ('Failed', 'Failed'),
    ('Unpaid', 'Unpaid'),
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Declined', 'Declined'),
    ('Settling', 'Settling'),
    ('Settled', 'Settled'),
    ('Cancelled', 'Cancelled'),
    ('Abandoned', 'Abandoned'),
    ('Refunded', 'Refunded'),
)


class Payment(models.Model):
    status=models.CharField(max_length=50,choices=PAYMENT_STATUS,default="Unshipped")
    amount=models.FloatField()
    order = models.OneToOneField(Order, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
