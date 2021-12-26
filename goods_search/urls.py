from django.urls import path, include, re_path
from goods_search import views

urlpatterns = [
    path(r'goods_search/',views.GoodsSearch.as_view()),
    path(r'merchant_search/',views.MerchantSearch.as_view()),
    path(r'detail/', views.Goods_detail.as_view()),
    path(r'comments/', views.Goods_comments.as_view()),
    path(r'addtocart/',views.add_to_cart.as_view()),
    path(r'inquiry/',views.customer_home.as_view())
]

