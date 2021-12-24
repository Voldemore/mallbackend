from django.urls import path
from cart import views

urlpatterns = [
    path(r'inquiry/', views.cart_inquiry.as_view()),
    path(r'delete/', views.carts_delete.as_view())
]