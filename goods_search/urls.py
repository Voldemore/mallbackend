from django.urls import path, include, re_path
from goods_search import views

urlpatterns = [
    path(r'goods_search/',views.GoodsSearch.as_view()),
    # path(r'merchant_search/',views.MerchantSearch.as_view())
]