from django.urls import path, include, re_path
from order_search import views

urlpatterns = [
    path(r'inquiry/',views.order_inquiry.as_view())

]
