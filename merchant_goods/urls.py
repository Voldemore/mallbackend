from django.urls import path
from merchant_goods import views

urlpatterns = [
    path(r'goods_search/', views.Goods_Bill.as_view()),
    path(r'addgoods/', views.Add.as_view()),
    path(r'delete/', views.Delete.as_view())
]