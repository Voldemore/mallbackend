from django.urls import path
from merchant_orders import views

urlpatterns = [
    path(r'orders/', views.Orders.as_view()),
    path(r'orderdetail/', views.OrderDetail.as_view()),
]