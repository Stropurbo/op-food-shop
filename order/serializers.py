from rest_framework import serializers
from order import models as ordermodel
from product.models import Product
from order.services import OrderServices

class EmptySerializer(serializers.Serializer):
    pass

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = ordermodel.CartItem
        fields = ['id', 'product_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = ordermodel.CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except ordermodel.CartItem.DoesNotExist:
            self.instance = ordermodel.CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError("Product Doesn't Exist")
        return value

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ordermodel.CartItem
        fields = ['quantity']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = ordermodel.CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item:ordermodel.CartItem):
        return cart_item.quantity * cart_item.product.price

class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name="get_total_price")
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ordermodel.Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']
    

    def get_total_price(self, cart:ordermodel.Cart):
        return sum(
            [item.quantity * item.product.price for item in cart.items.all() ]
        ) 

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = self.validated_data['cart_id']

        try:
            order = OrderServices.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
    def to_representation(self, instance):
        return OrderSerializer(instance).data
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = ordermodel.OrderItem
        fields = ['id', 'product', 'price', 'quantity', 'total_price']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ordermodel.Order
        fields = ['status']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)

    class Meta:
        model = ordermodel.Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']


    


