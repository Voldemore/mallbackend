from django.urls import path, include, re_path
from goods_search import views

urlpatterns = [
    path(r'detail/',views.GoodsSearch.as_view())

]