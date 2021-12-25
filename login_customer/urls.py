#python manage.py runserver 0.0.0.0:8000
from django.urls import path
from login_customer import views

urlpatterns = [
    path(r'register/', views.Register.as_view()),
    path(r'login/', views.Login.as_view()),
    path(r'info_modification/', views.Info_Mod.as_view()),
    path(r'address/', views.Receive_Address.as_view()),
    path(r'addaddress/', views.Add_Receive_address.as_view())
]

