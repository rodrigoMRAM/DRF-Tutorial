from django.db import models
from rest_framework import generics , serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your models here.

class Product(models.Model):
    usuario =  models.TextField(max_length=250, verbose_name="Username")
    name = models.CharField(max_length=50)

class ProductSerializer(serializers.ModelSerializer):
    Meta: Product
    fields = ['usuario']


class VerProducto(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'usuario'


@api_view(['GET'])
def create_function(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_function(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



