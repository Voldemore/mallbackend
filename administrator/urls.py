from django.urls import path
from administrator import views

urlpatterns=[
    path(r'login/', views.Login.as_view()),
    path(r'allmer_search/',views.all_merchants.as_view())
]