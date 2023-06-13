from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..serializers import UserSerializer, UserSerializerWithToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, IsAdminUser



@api_view(['GET'])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def login(request):
    data = request.data
    username = data['email']
    password = data['password']

    try:
        user = User.objects.get(username=username)
    except:
        return Response({'detail': 'User with this email does not exist'}, status=400)
    
    # check if the password is correct
    if not user.check_password(password):
        return Response({'detail': 'Invalid password'}, status=400)
    
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def register_user(request):

    data = request.data
    try:
        user = User.objects.create_user(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password =make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=400) 


# get users 
@api_view(['GET'])
# @permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
    
    user.save()
    # even if the serializer is defined before the user update, 
    # it will still return the updated user, because the serializer is not called until the return statement
    return Response(serializer.data)
    
