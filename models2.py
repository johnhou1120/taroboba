from datetime import timedelta, date
from pyexpat import model
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
# Create your models here.

class Payment(models.Model):
    short = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    # Metadata
    class Meta:
        ordering = ['short']

    def __str__(self):
        return self.name


class Store(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    storeid = models.CharField(max_length=25,unique=True, primary_key= True)
    name = models.CharField(max_length=25)
    address = models.TextField(blank= True, null= True)
    phone = models.CharField(max_length=20, blank= True, null= True)
    payment = models.ManyToManyField(Payment)
    state = models.BooleanField(default=False)
    comments = models.TextField(blank= True, null= True)

    # Metadata
    class Meta:
        ordering = ['storeid']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


class Users(models.Model):
    # Fields
    lineid = models.CharField(max_length=50, unique=True, primary_key= True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=20, blank= True, null= True)
    address = models.TextField(blank= True, null= True)
    birthday = models.DateTimeField(blank= True, null= True)
    followdate = models.DateTimeField(default=timezone.now)
    mambercard = models.CharField(blank= True, null= True)
    einvoice = models.CharField(blank= True, null= True)

    # Metadata
    class Meta:
        ordering = ['-followdate']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


class ProdGroups(models.Model):
    # Fields
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=25)
    comments = models.TextField(blank= True, null= True)

    # Metadata
    class Meta:
        ordering = ['code']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

class Ingredients(models.Model):
    # Fields
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    options = models.TextField(blank= True, null= True , help_text='input options, separated by [,]')

    # Metadata
    class Meta:
        ordering = ['code']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

class Products(models.Model):
    # Fields
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank= True, null= True)
    group = models.ForeignKey(ProdGroups,related_name='group', to_field='code',on_delete=models.CASCADE)
    comments = models.TextField(blank= True, null= True)
    state = models.BooleanField(default=False)
    enableingredients = models.ManyToManyField(Ingredients, related_name='enableingredients', to_field='code', on_delete=models.CASCADE, blank= True, null= True)

    # Metadata
    class Meta:
        ordering = ['code']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


class ActivityType(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    comments = models.TextField(blank=True, null =True)

# Metadata
    class Meta:
        ordering = ['code']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

class Activity(models.Model):
    # Fields
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    type = models.ForeignKey(ActivityType, to_field='code', on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null =True)
    startdate = models.DateField(default=date.today)
    duedate = models.DateField(default=date.today)

    # Metadata
    class Meta:
        ordering = ['code']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name
    
    def get_state(self):
        if self.startdate <= timezone.now < self.duedate + timedelta(1):
            return True
        else:
            return False

class Coupon(models.Model): 
    code = models.CharField(max_length=20, primary_key=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, to_field='code', related_name='activity')
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='lineid', related_name='owner')
    discount_percent = models.FloatField(blank=True, null= True)
    discount_amount = models.FloatField(blank=True, null= True)
    miniconsump = models.FloatField(blank=True, null= True)
    used = models.BooleanField(default=False)
    duedate = models.DateTimeField(delault = date.today + timedelta(90))

    def __str__(self):
        return self.code


class Order(models.Model):
    PickupOptions = (('Pickup', '自取'), ('Delivery', '外送'))
    OrderStatusOptions = (('ordering', '訂購中'), ('sending', '下單中'), ('preparing','接單準備中'), ('ready', '準備就緒'), ('delivering', '外送中'), ('finished', '訂單完成'))
    InvoiceOption = (('P', '實體發票'), ('M', '會員載具'), ('E', '手機載具'), ('D', '愛心捐贈'))
    
    # Fields
    ordernumber = models.CharField(max_length=50, unique=True, primary_key=True)
    orderer = models.ForeignKey(Users, on_delete= models.CASCADE, to_field='lineid', related_name='orderer')
    paymethod = models.ForeignKey(Payment, on_delete= models.CASCADE, to_field='short', blank= True, null= True, related_name='paymethod')
    pickupmethod = models.CharField(max_length=20, choices=PickupOptions, blank= True, null= True)
    status = models.CharField(max_length= 20, choices=OrderStatusOptions, default='ordering')
    paystate = models.BooleanField(default=False)
    receiver = models.CharField(max_length=20, blank= True, null= True)
    receiverphone = models.CharField(max_length=20, blank= True, null= True)
    receiveraddress = models.TextField(blank= True, null= True)
    invoice = models.CharField(max_length=1, choices=InvoiceOption, default='P')
    groupbuy = models.CharField(max_length=20, unique = True, blank=True, null = True)
    voucheruse= models.ForeignKey(Coupon, on_delete= models.CASCADE, to_field='code', blank= True, null= True, related_name='voucheruse')

    # Metadata
    class Meta:
        ordering = ['ordernumber']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.ordernumber

class GroupBuyList(models.Model):
    # Fields
    listnumber = models.CharField(max_length=50, unique=True, primary_key=True)
    member = models.ForeignKey(Users, on_delete= models.CASCADE, to_field='lineid', related_name='member')
    groupbuynmber = models.ForeignKey(Order, to_field='groupbuy')
    message = models.TextField(blank= True, null= True)
    voucheruse= models.ForeignKey(Coupon, on_delete= models.CASCADE, to_field='code', blank= True, null= True, related_name='voucheruse')

    # Metadata
    class Meta:
        ordering = ['listnumber']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.listnumber

class ItemsList(models.Model):
    # Fields
    ordernumber = models.ForeignKey(Order, on_delete=models.CASCADE, blank= True, null= True)
    listnumber = models.ForeignKey(GroupBuyList, on_delete=models.CASCADE, blank= True, null= True)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    addition = models.TextField(blank= True, null= True)
    quantity = models.IntegerField(default=1)

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()