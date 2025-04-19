from order.models import Cart, Order, OrderItem
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

class OrderServices:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk = cart_id)
            cart_items = cart.items.select_related('product').all()

            total_price = sum([item.quantity * item.product.price for item in cart_items])
            order = Order.objects.create(user_id=user_id, total_price=total_price)

            oder_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity,
                    total_price = item.product.price * item.quantity
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(oder_items)
            cart.delete()
            return order
        
    @staticmethod
    def cancel_order(order, user):
        if user.is_staff:
            order.status = Order.CANCELED
            order.save()
            return order
        if order.user != user:
            raise PermissionDenied("You can cancel your own order.")
        
        if order.status == Order.DELIVERED:
            raise ValidationError("You can't cancel the order.")
        
        order.status = Order.CANCELED
        order.save()
        return order
        
