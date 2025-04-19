from django.urls import path, include
from rest_framework_nested import routers
from product import views
from order import views as allOrder

router = routers.DefaultRouter()
router.register('products', views.ProductViewset, basename='products')
router.register('category', views.CategoryViewset)
router.register('carts', allOrder.CartView, basename="carts")
router.register('orders', allOrder.OrderView, basename="orders")

product_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
product_router.register('images', views.ProductImageViewset, basename="product-images")
product_router.register('review', views.ReviewViewset, basename="product-review")

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', allOrder.CartItemView, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
]
