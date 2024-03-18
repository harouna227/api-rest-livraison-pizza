from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderCreateListView.as_view(), name='orders'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='orders-detail'),
    path('order-status/<int:pk>/', views.UpdateStatusView.as_view(), name='update-order-status'),
    path('user/<int:user_id>/orders/', views.UserOrderView.as_view(), name='user-orders'),
    path('user/<int:user_id>/order/<int:order_id>/', views.UserOrderDetail.as_view(), name='user-special-detail'),
]

