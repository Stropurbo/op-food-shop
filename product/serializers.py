from rest_framework import serializers
from decimal import Decimal
from product import models

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'description', 'product_count']

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = models.ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    class Meta:
        model = models.Product
        fields = ['id', 'name', 'description', 'price', 'price_with_tax' ,'category','discount_price','created_at', 'updated_at', 'images']

    
    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2)

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price not less than 0.")
        return price
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.discount_price is None:
            data.pop('discount_price')
        return data

    
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = ['id', 'user', 'product', 'ratings', 'comment']
        read_only_fields = ['product', 'user']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        review = models.Review.objects.create(product_id=product_id, **validated_data)
        return review
    
    def get_user(self, obj):
        return obj.user.get_full_name()
    
    def get_product(self, obj):
        return obj.product.name