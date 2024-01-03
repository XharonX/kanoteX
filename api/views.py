from django.shortcuts import render
from productions.serializers import ProductSerializer
from productions.models import Product
from rest_framework import viewsets

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('code')
    serializer_class = ProductSerializer