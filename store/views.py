import collections
from decimal import Context
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, request
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from store.permissions import IsAdminOrReadOnly

from .filters import ProductFilter
from .pagination import DefaultPagination
from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, Review
from .serializers import  AddCartItemSerializer, CartItemSerializer, CartSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer
# Create your views here.

#read about all imported classes online


#1st implementation
''' This is a function based view this can also be converted to a class based view as below
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(query_set, many=True, context = {'request' : request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''

#2nd implementation
'''class ProductList(APIView):

    def get(self, request):  
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(query_set, many=True, context = {'request' : request})
        return Response(serializer.data)

    def post(self, request): 
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''

#3rd implementation
'''
class ProductList(ListCreateAPIView):
    queryset  = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request' : self.request}
'''

'''
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    #try:
    #    product = Product.objects.get(pk=id)
    #    serializer = ProductSerializer(product)
    #    return Response(serializer.data)
    #except Product.DoesNotExist:
    #    return Response(status=status.HTTP_404_NOT_FOUND)

    product = get_object_or_404(Product, pk=id)
    if(request.method == 'GET'):
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif(request.method == 'DELETE'):
        if(product.orderitems.count() > 0):
            return Response({'error':'cant be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status.HTTP_204_NO_CONTENT)
'''
'''
class ProductDetail(APIView):
    
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if(product.orderitems.count() > 0):
            return Response({'error':'cant be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status.HTTP_204_NO_CONTENT)
'''

'''
class ProductDetail(RetrieveUpdateDestroyAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if(product.orderitems.count() > 0):
            return Response({'error':'cant be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status.HTTP_204_NO_CONTENT)
'''

#here we're combining both productlist and product detail views in one
class ProductViewSet(ModelViewSet):
    queryset  = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if(OrderItem.objects.filter(product_id = kwargs['pk']).count()):
            return Response({'error':'cant be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



'''
@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        query_set = Collection.objects.annotate(products_count = Count('product')).all()
        serializer = CollectionSerializer(query_set, many=True, context = {'request' : request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''

'''
class CollectionList(APIView):

    def get(self, request):
        query_set = Collection.objects.annotate(products_count = Count('product')).all()
        serializer = CollectionSerializer(query_set, many=True, context = {'request' : request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''




'''
@api_view(['GET','PUT','DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count = Count('product')), pk=pk)

    if(request.method == 'GET'):
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif(request.method == 'DELETE'):
        if(collection.products_count > 0):
            return Response({'error':'cant be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status.HTTP_204_NO_CONTENT)
'''

'''
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count = Count('product'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Product, pk=pk)
        if(collection.products_count > 0):
            return Response({'error':'cant be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status.HTTP_204_NO_CONTENT)
'''

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('product')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    def delete(self, request, pk):
        collection = get_object_or_404(Product, pk=pk)
        if(collection.products_count > 0):
            return Response({'error':'cant be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet, DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    #serializer_class = CartItemSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']

    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).select_related('product')

class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET','PUT'])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
