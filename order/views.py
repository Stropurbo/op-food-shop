from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from order.models import Cart, CartItem, Order
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from order import serializers as ordersz
from rest_framework.decorators import action
from order.services import OrderServices
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class CartView(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    API endpoints for Product Cart 
    - only admin can manage the Cart with all features
    - Authenticated product buyer can cart product unauthenticate users not.
    """   
   
    serializer_class = ordersz.CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').filter(user = self.request.user)
    
    def get_object(self):
        return get_object_or_404(Cart, user= self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
class CartItemView(ModelViewSet):
    """
    API endpoints for Product Cart items
    - only admin can manage the Cartitems with all features
    - Authenticated product buyer can see their cart items what they cart
    """

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ordersz.AddToCartSerializer
        elif self.request.method == "PATCH":
            return ordersz.UpdateCartItemSerializer
        return ordersz.CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk')}
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs.get('cart_pk'))
    
class OrderView(ModelViewSet):
    """
    API endpoints for OrderView
    - only admin can manage the Order with all features
    - Authenticated product buyer can order product also they can add or remove
    product from the order item and also they can cancel order before the item is delivered
    """

    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderServices.cancel_order(order=order, user=request.user)
        return Response({'status': 'Order Canceled'})
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = ordersz.UpdateOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Order Status Updated")
    
    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'cancel':
            return ordersz.EmptySerializer
        if self.action == 'create':
            return ordersz.CreateOrderSerializer
        elif self.action == 'update_status':
            return ordersz.UpdateOrderSerializer
        return ordersz.OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user': self.request.user}
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related("items__product").all()
        return Order.objects.prefetch_related('items__product').filter(user = self.request.user)

