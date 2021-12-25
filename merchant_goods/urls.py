from django.urls import path
from merchant_goods import views

urlpatterns = [
    path(r'addgoods/', views.Add.as_view()),
    path(r'delete/', views.Delete.as_view()),
    path(r'alter/', views.Alter.as_view()),
]