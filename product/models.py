from django.db import models
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    order = models.PositiveSmallIntegerField(verbose_name='Order')

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(to='product.Category', on_delete=models.CASCADE, related_name='product',
                                 verbose_name="Category")
    title = models.CharField(max_length=100, verbose_name='Title')
    slug = models.CharField(max_length=100, verbose_name='Slug')
    price = models.DecimalField(verbose_name="Price", max_digits=5, decimal_places=2)
    description = models.TextField(verbose_name='Description')
    is_published = models.BooleanField(verbose_name="Published")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    product = models.ManyToManyField(to=Product, related_name='tag', verbose_name="Products")

    def __str__(self):
        return self.title


class CartItem(models.Model):
    product = models.ForeignKey(to='product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name="Quantity", blank=True)
    order = models.PositiveSmallIntegerField(verbose_name='Order', blank=True)
    active = models.BooleanField(verbose_name="Active")
    cart = models.ForeignKey(to='product.Cart', related_name='items', verbose_name='Cart', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product}"


class Cart(models.Model):
    owner = models.OneToOneField(to='user.User', verbose_name='Owner', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.first_name}'s cart"

