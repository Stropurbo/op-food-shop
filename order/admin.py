from django.contrib import admin
from order import models

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'status']


admin.site.register(models.CartItem)
admin.site.register(models.OrderItem)