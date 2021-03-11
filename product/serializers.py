from django.db.models import Sum
from rest_framework import serializers

from product.models import Category, Tag, CartItem, Product, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'order']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['title', 'product']
        extra_kwargs = {
            'product': {"write_only": True},
        }


class ProductSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'description', 'is_published', 'category', 'tag']

        extra_kwargs = {
            'category': {"write_only": True},
            'slug': {'read_only': True},
        }


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'description', 'is_published', 'category', 'tag']


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'order', 'active', 'cart']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_cost = serializers.SerializerMethodField()

    def get_total_cost(self, obj):
        cart_items = CartItem.objects.filter(cart=obj)
        total_price = 0
        for item in cart_items:
            total_price += item.quantity*item.product.price
        return total_price

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cost']
