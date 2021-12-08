from django.urls import path, include, re_path
from order_search import views

urlpatterns = [
    path(r'goods_search/',views.GoodsSearch.as_view())

]