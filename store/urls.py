from django.urls import path
from django.urls.resolvers import URLPattern
from rest_framework import routers, urlpatterns
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet) 
router.register('customers', views.CustomerViewSet) 
router.register('orders' , views.OrderViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup= 'cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + cart_router.urls

'''
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail')
]
'''