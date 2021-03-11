from django.urls import path, include
from user import views

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('user/<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
    path('register/', views.RegistrationView.as_view(), name='register'),
]
