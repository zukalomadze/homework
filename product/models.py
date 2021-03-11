from django.db import models


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    order = models.CharField(max_length=100, verbose_name='Order')


class Product(models.Model):
    category = models.ForeignKey(to='product.Category', on_delete=models.CASCADE, related_name='product',
                                 verbose_name="Category")
    title = models.CharField(max_length=100, verbose_name='Title')
    slug = models.CharField(max_length=100, verbose_name='Slug')
    price = models.DecimalField(verbose_name="Price", max_digits=5, decimal_places=2)
    description = models.TextField(verbose_name='Description')
    is_published = models.BooleanField(verbose_name="Published")


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    product = models.ManyToManyField(to=Product, related_name='tag', verbose_name="Products")


class CartItem(models.Model):
    product = models.ForeignKey(to='product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name="Quantity")
    order = models.CharField(max_length=100, verbose_name="Order")
    active = models.BooleanField(verbose_name="Active")
    cart = models.ForeignKey(to='product.Cart', related_name='items', verbose_name='Cart')


class Cart(models.Model):
    owner = models.OneToOneField(to='user.User', verbose_name='Owner', on_delete=models.CASCADE)
