from django.urls import path

from . import views

urlpatterns = [
    path('', views.HelloOrders.as_view())
]