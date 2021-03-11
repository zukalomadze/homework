from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'cart', views.CartViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]