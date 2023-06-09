
# Create your models here.
# create Product model 
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # if user is deleted, set product to null
    name = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    image =  models.ImageField(null=True, blank=True, default='/placeholder.png')
    brand = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True) # null=True means it is not required
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # decimal_places=2 means 2 decimal places
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # decimal_places=2 means 2 decimal places
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True) # auto_now_add=True means it will automatically add the date when the product is created
    _id = models.AutoField(primary_key=True, editable=False) # _id is the primary key


    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # if product is deleted, set review to null
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # if user is deleted, set review to null
    name = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True) # auto_now_add=True means it will automatically add the date when the product is created
    _id = models.AutoField(primary_key=True, editable=False) # _id is the primary key


    def __str__(self):
        return str(self.rating)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # if user is deleted, set order to null
    paymentMethod = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # decimal_places=2 means 2 decimal places
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # decimal_places=2 means 2 decimal places
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # decimal_places=2 means 2 decimal places
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True) # auto_now_add=True means it will automatically add the date when the product is created
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True) # auto_now_add=True means it will automatically add the date when the product is created
    createdAt = models.DateTimeField(auto_now_add=True) # auto_now_add=True means it will automatically add the date when the product is created
    _id = models.AutoField(primary_key=True, editable=False) # _id is the primary key


    def __str__(self):
        return str(self.createdAt)
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # if product is deleted, set order item to null
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) # if order is deleted, set order item to null
    name = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # decimal_places=2 means 2 decimal places
    image = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    _id = models.AutoField(primary_key=True, editable=False) # _id is the primary key


    def __str__(self):
        return self.name
    
class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True) # if order is deleted, set shipping address to null
    address = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    city = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    postalCode = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    country = models.CharField(max_length=200, null=True, blank=True) # blank=True means it is not required
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # decimal_places=2 means 2 decimal places
    _id = models.AutoField(primary_key=True, editable=False) # _id is the primary key


    def __str__(self):
        return self.address