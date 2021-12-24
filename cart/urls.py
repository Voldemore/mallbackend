from django.urls import path
from cart import views

urlpatterns = [
    path(r'query/', views.cart_query.as_view())
]