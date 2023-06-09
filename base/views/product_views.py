from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models import Product
from ..serializers import ProductSerializer
#  import user model
#  imoort make password

from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def getProducts(request):
    
    products = Product.objects.all() 
    #  we need to serialize the data
    # many=True because we are returning multiple objects
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
    # return Response(products)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    ser = ProductSerializer(product, many=False)
    return Response(ser.data)


@api_view(['POST'])
def createProduct(request):
    data = request.data
    # serializer = ProductBodySerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    # else :
    #     return Response(serializer.errors)
    product = Product.objects.create(
        name = data['name'],
        price = data['price'],
        brand = data['brand'],
        countInStock = data['countInStock'],
        category = data['category'],
        description = data['description'],
        rating = data['rating'],
        numReviews = data['numReviews'],
        image = data['image'],
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)
