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
    CartSerializer, CreateProductSerializer


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
    permission_classes = [IsAdminUserOrReadOnly]

    serializer_action = {
        'create': CreateProductSerializer,
        'update': CreateProductSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action.get(getattr(self, 'action', None), self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, *args, **kwargs):
        cart = Cart.objects.filter(owner=request.user).get()
        product = self.get_object()
        quantity = self.request.data.get('quantity', 1)
        data = {'product': product,
                'active': True,
                'order': product.pk,
                'cart': cart,
                'quantity': quantity,
                }
        CartItem.objects.create(**data)
        return Response({'product': reverse('product-list', request=request)})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
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
        # response = requests.post('https://hooks.slack.com/services/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',
        #                          json=data)
        return Response(data)