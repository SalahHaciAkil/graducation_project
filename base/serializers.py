# 
# 
# 
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# Serializers, similar to mappers, they are used to convert data to JSON format
# 
# 
# 
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken    
from .models import Product, Review, Order, OrderItem, ShippingAddress

# serializers for the models
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' # all fields
    
class UserSerializer(serializers.ModelSerializer):
    name =serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', '_id', 'isAdmin']

    def get_name(self, obj):
        name = obj.first_name + ' ' + obj.last_name
        if name == ' ':
            name = obj.email

    def get__id(self, obj):
        _id = obj.id
        return _id
    
    def get_isAdmin(self, obj):
        isAdmin = obj.is_staff
        return isAdmin

         # all fields
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', '_id', 'isAdmin', 'token']

    def get_token(self, obj):
        print("The Token Is :")
        print(obj)
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__' # all fields

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class ProductBodySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    brand = serializers.CharField(max_length=200)
    countInStock = serializers.IntegerField()
    category = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    rating = serializers.DecimalField(max_digits=7, decimal_places=2)
    numReviews = serializers.IntegerField()
    image = serializers.ImageField()
     

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data