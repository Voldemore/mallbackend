from django.urls import path
from login_merchant import views

urlpatterns = [
    path(r'register/', views.Register.as_view()),
    path(r'login/', views.Login.as_view()),
    path(r'merinfo/', views.Merchant_Info.as_view()),
    path(r'home/', views.Home.as_view()),
]
