from datetime import timedelta, date
from pyexpat import model
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
# Create your models here.

class Payment(models.Model):
    short = models.CharField(max_length=10, unique= True)
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

    def display_payment_method(self):
        return ';'.join(payment.name for payment in self.payment.all())

    display_payment_method.short_description = 'Payment'

class Users(models.Model):
    # Fields
    lineid = models.CharField(max_length=50, unique=True, primary_key= True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=20, blank= True, null= True)
    address = models.TextField(blank= True, null= True)
    birthday = models.DateField(blank= True, null= True)
    followdate = models.DateTimeField(default=timezone.now)
    mambercard = models.CharField(max_length= 25, blank= True, null= True)
    einvoice = models.CharField(max_length= 25, blank= True, null= True)

    # Metadata
    class Meta:
        ordering = ['-followdate']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


class Category(models.Model):
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

class Options(models.Model):
    # Fields
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    price = models.PositiveIntegerField()

    # Metadata
    class Meta:
        ordering = ['code']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return ":".join(self.type, self.name)

class Products(models.Model):
    # Fields
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    category = models.ForeignKey(Category,related_name='category', to_field='code',on_delete=models.CASCADE)
    comments = models.TextField(blank= True, null= True)
    image = models.ImageField(null= True)
    state = models.BooleanField(default=False)
    enableoptions = models.ManyToManyField(Options, blank=True)

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
    duedate = models.DateField(default = date.today() + timedelta(90))

    def __str__(self):
        return self.code

class OrderItems(models.Model):
    # Fields
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    addition = models.ManyToManyField(Options)
    quantity = models.IntegerField(default=1)

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        total = self.quantity * self.item.price
        for add in self.addition:
            total + add.price
        return total

    def get_total_discount_item_price(self):
        total = self.quantity * self.item.discount
        for add in self.addition:
            total + add.price
        return total

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def display_addtions(self):
        return '/'.join(add.name for add in self.addition.all())

    display_addtions.short_description = 'Additions'

class Grouping(models.Model):
    # Fields
    ref_code = models.CharField(max_length=50, unique=True, primary_key=True)
    user = models.ForeignKey(Users, on_delete= models.CASCADE, to_field='lineid', related_name='g_user')
    items = models.ManyToManyField(OrderItems)
    message = models.TextField(blank= True, null= True)
    coupon= models.ForeignKey(Coupon, on_delete= models.SET_NULL, to_field='code', blank= True, null= True, related_name='g_coupon')

    # Metadata
    class Meta:
        ordering = ['ref_code']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.ref_code

    def get_total_quantity(self):
        quantity = 0
        for order_item in self.items.all():
            quantity += order_item.quantity
        return quantity 

    def get_total_amount(self):
        total = 0
        diff_4_coupon = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            if total >= self.coupon.miniconsump:
                total -= self.coupon.discount_amount
            else:
                diff_4_coupon = self.coupon.miniconsump - total
        return total, diff_4_coupon

class Order(models.Model):
    PickupOptions = (('Pickup', '自取'), ('Delivery', '外送'))
    OrderStatusOptions = (('ordering', '訂購中'), ('sending', '下單中'), ('preparing','接單準備中'), ('ready', '準備就緒'), ('delivering', '外送中'), ('finished', '訂單完成'))
    InvoiceOption = (('P', '實體發票'), ('M', '會員載具'), ('E', '手機載具'), ('D', '愛心捐贈'))
    
    # Fields
    ref_code = models.CharField(max_length=50, unique=True, primary_key=True)
    user = models.ForeignKey(Users, on_delete= models.CASCADE, to_field='lineid', related_name='o_user')
    items = models.ManyToManyField(OrderItems)
    paymethod = models.ForeignKey(Payment, on_delete= models.SET_NULL, to_field='short', blank= True, null= True, related_name='paymethod')
    pickupmethod = models.CharField(max_length=20, choices=PickupOptions, blank= True, null= True)
    status = models.CharField(max_length= 20, choices=OrderStatusOptions, default='ordering')
    paystate = models.BooleanField(default=False)
    receiver = models.CharField(max_length=20, blank= True, null= True)
    receiverphone = models.CharField(max_length=20, blank= True, null= True)
    receiveraddress = models.TextField(blank= True, null= True)
    invoice = models.CharField(max_length=1, choices=InvoiceOption, default='P')
    isgrouping = models.BooleanField(default=False)
    groupmamber = models.ManyToManyField(Grouping)
    coupon= models.ForeignKey(Coupon, on_delete= models.SET_NULL, to_field='code', blank= True, null= True, related_name='o_coupon')

    # Metadata
    class Meta:
        ordering = ['ref_code']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.ref_code

    def get_total_quantity(self):
        quantity = 0
        for order_item in self.items.all():
            quantity += order_item.quantity
        if self.isgrouping:
            for mamber in self.groupmamber.all():
                quantity += mamber.get_total_quantity()
        return quantity 

    def get_total_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.isgrouping:
            for mamber in self.groupmamber.all():
                total_4_mamber, _ = mamber.get_total_amount()
                total+= total_4_mamber
        diff_4_coupon = 0
        if self.coupon:
            if total >= self.coupon.miniconsump:
                total -= self.coupon.discount_amount
            else:
                diff_4_coupon = self.coupon.miniconsump - total
        return total, diff_4_coupon
