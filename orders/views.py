from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderCreationSerializer, OrderDetailSerializer
from .models import Order


# Create your views here.    
class OrderCreateListView(generics.GenericAPIView):
    
    queryset = Order.objects.all()
    serializer_class = OrderCreationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        pass

    def post(self, request, pk):
        pass