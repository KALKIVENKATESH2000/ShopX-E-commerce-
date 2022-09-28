from app.models import *
from rest_framework import generics
from .serializers import *

class ListProduct(generics.ListCreateAPIView):
    queryset =Product.objects.all()
    serializer_class = ProductSerializer

class DetailProduct(generics.RetrieveUpdateDestroyAPIView):
    queryset =Product.objects.all()
    serializer_class = ProductSerializer

class ListUser(generics.ListCreateAPIView):
    queryset =User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset =User.objects.all()
    serializer_class = UserSerializer

class ListCart(generics.ListCreateAPIView):
    queryset =Cart.objects.all()
    serializer_class = CartSerializer

class DetailCart(generics.RetrieveUpdateDestroyAPIView):
    queryset =Cart.objects.all()
    serializer_class = CartSerializer

class ListOrder(generics.ListCreateAPIView):
    queryset = OrderPlaced.objects.all()
    serializer_class = OrderSerializer

class DetailOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset =OrderPlaced.objects.all()
    serializer_class = OrderSerializer