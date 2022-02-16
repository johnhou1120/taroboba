from django.contrib import admin
from store.models import *
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('short', 'name')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('storeid', 'name', 'display_payment_method', 'state')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('lineid', 'name', 'phone', 'followdate')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'type', 'price')

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price', 'discount', 'category', 'state')

@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'type', 'startdate', 'duedate')
    # fields 參數 可以自訂編輯畫面中的排列順序
    # ()中的 代表顯示在同一列
    fields = ['code', 'name', 'type', 'comments', ('startdate', 'duedate')]

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'activity', 'owner', 'discount_amount')

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_addtions')

@admin.register(Grouping)
class GroupingAdmin(admin.ModelAdmin):
    list_display = ('ref_code', 'user')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref_code', 'user', 'status', 'paystate', 'isgrouping')
    # 將編輯欄位分區塊顯示
    fieldsets = (
        (None, {
            'fields': ['ref_code', 'user']
        }),
        ('清單', {
            'fields': ['items']
        }),
        ('狀態', {
            'fields': [('paymethod',  'paystate'), ('pickupmethod', 'status'), 'invoice', 'coupon']
        }),
        ('收件人', {
            'fields': [('receiver', 'receiverphone'), 'receiveraddress']
        }),
        ('團購', {
            'fields': ['isgrouping', 'groupmamber']
        }),
    )

