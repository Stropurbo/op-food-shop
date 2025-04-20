from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from product import serializers
from product import models
from product.permissions import AuthorOrReadOnly, AdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from django.db.models import Count
from rest_framework.exceptions import PermissionDenied

class ProductViewset(ModelViewSet):

    """
    API endpoints for managing products 
    - only admin can manage product with all features.
    - others user can only browser and order product
    - support searching by name, des, category, price and ordering
    """

    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class  = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price']
    permission_classes = [AdminOrReadOnly]

    def get_queryset(self):
        queryset =  models.Product.objects.prefetch_related('images').all()
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Retriving all product
        """
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
        only admin can manage product.
        """
        return super().create(request, *args, **kwargs)
    


class ProductImageViewset(ModelViewSet):
    """
    API endpoints for Image view 
    - only admin can manage image.
    - others user see image with product
    """
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [AdminOrReadOnly]

    def get_queryset(self):
        return models.ProductImage.objects.filter(product_id = self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        serializer.save(product_id= self.kwargs.get('product_pk'))  

class CategoryViewset(ModelViewSet):
    """
    API endpoints for Product Category 
    - only admin can manage the category with create, update, delete
    - others user see the category wise product
    """
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.annotate(product_count = Count('products')).all()
    permission_classes = [AdminOrReadOnly]

class ReviewViewset(ModelViewSet):
    """
    API endpoints for Product Review 
    - only admin can manage Review section with create, update, delete
    - Authenticated user can review the product.
    """

    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated and AuthorOrReadOnly]

    def get_queryset(self):
        return models.Review.objects.filter(product_id = self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}
    
    def perform_create(self, serializer):
        if not self.request.user or not self.request.user.is_authenticated:
            raise PermissionDenied("Please login first.")
        return serializer.save(user=self.request.user)
