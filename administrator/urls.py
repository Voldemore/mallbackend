from django.urls import path
from administrator import views

urlpatterns=[
    path(r'login/', views.Login.as_view()),
    path(r'allmer_search/',views.all_merchants.as_view()),
    path(r'goods_search/',views.GoodsSearchKeywords.as_view()),
    path(r'mer_search/',views.MerchantSearchKeywords.as_view()),
    path(r'user_order_search/',views.UserOrderSearch.as_view()),
    path(r'user_goods_search/',views.UserGoodsSearch.as_view()),
    path(r'user_province_search/', views.user_province_search.as_view())
]