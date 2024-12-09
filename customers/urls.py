from . import views
from django.urls import path

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("", views.update_customer, name="customer_Detail"),
]
