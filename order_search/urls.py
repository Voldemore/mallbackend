from django.urls import path
from order_search import views

urlpatterns = [
    path(r'inquiry/', views.order_inquiry.as_view()),
    path(r'orderdetail/', views.order_details.as_view()),
    path(r'received/',views.order_state.as_view()),
    path(r'postcomments/',views.comments_release.as_view())
]
