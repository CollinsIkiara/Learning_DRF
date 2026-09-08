from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all() # queryset of all products
    serializer = ProductSerializer(products, many=True) # many =True because we are serializing a queryset of multiple products
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk) # get the product with the given primary key
    serializer = ProductSerializer(product) # serialize the product
    return Response(serializer.data)