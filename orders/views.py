from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from .serializers import (
    OrderCreationSerializer, 
    OrderDetailSerializer,
    OrderStatusUpdateSerializer,
)
from .models import Order


CustomerUser = get_user_model()

# Create your views here.    
class OrderCreateListView(generics.GenericAPIView):
    
    queryset = Order.objects.all()
    serializer_class = OrderCreationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary='List all orders')
    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary='Create a new order')
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary='Retreive an order')
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary='Update an order')
    def put(self, request, pk):
        user = request.user
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=order)
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary='Delete an order')
    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UpdateStatusView(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary='Update a status order')
    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserOrderView(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer

    @swagger_auto_schema(operation_summary='Get all orders for a user')
    def get(self, request, user_id):
        user = CustomerUser.objects.get(pk=user_id)
        order = Order.objects.all().filter(customer=user)
        serializer = self.serializer_class(instance=order, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)   

class UserOrderDetail(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer

    @swagger_auto_schema(operation_summary='Get a user specific orders')
    def get(self, request, user_id, order_id):
        user = CustomerUser.objects.get(pk=user_id)
        orders = Order.objects.all().filter(customer=user).filter(pk=order_id)
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
