"""mallbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from goods_search import views
from login_customer import views
from django.contrib import admin

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/customer/', include('login_customer.urls')),
    path(r'api/orders/', include('order_search.urls')),
    path(r'api/goods_search/', include('goods_search.urls')),
    path(r'api/merchant/', include('login_merchant.urls')),
    path(r'api/cart', include('cart.urls')),
    path(r'api/query', include('query.urls')),
]
