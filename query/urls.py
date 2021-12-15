from django.urls import path, include, re_path
from query import views

urlpatterns = [
    path(r'a/',views.MerQuery.as_view()),
    path(r'b/',views.GoodsQuery.as_view())
]