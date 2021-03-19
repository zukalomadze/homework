from django.shortcuts import render
from rest_framework import viewsets, filters, permissions, views, generics, mixins

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from product.models import Category, Product, Tag, CartItem, Cart
from product.permissions import IsAdminUserOrReadOnly, IsOwner
from product.serializers import CategorySerializer, ProductSerializer, TagSerializer, CartItemSerializer, \
    CartSerializer, CreateProductSerializer, AddToCartSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('order')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    default_serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category', 'price']
    search_fields = ['title']
    # permission_classes = [IsAdminUserOrReadOnly]

    serializer_action = {
        'create': CreateProductSerializer,
        'update': CreateProductSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action.get(getattr(self, 'action', None), self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'], default_serializer_class=AddToCartSerializer)
    def add_to_cart(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=request.user.cart,
                            product=self.get_object(),
                            order=self.get_object().pk,
                            active=True,)
        return Response({'message': "Item Successfully added to cart"})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    #@TODO reorder


class CartViewSet(mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsOwner]

    @action(detail=True, url_path='checkout', methods=['get'])
    def checkout(self, request, *args, **kwargs):
        import requests
        data = {
            'text': 'Hello World'
        }

        return Response(data)
