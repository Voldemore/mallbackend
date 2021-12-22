from django.urls import path
from login_merchant import views

urlpatterns = [
    path(r'register/', views.Register.as_view()),
    path(r'login/', views.Login.as_view()),
    path(r'merinfo/', views.Merchant_Info.as_view()),
    path(r'merhome/', views.Goods_Search.as_view()),
    path(r'goods_search/', views.Goods_Bill.as_view())
]
