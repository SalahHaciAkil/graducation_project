# urls.py 

from django.urls import path
from base.views import user_views as views    
from rest_framework_simplejwt.views import (
    TokenObtainPairView,

)
from base.serializers import CustomTokenObtainPairSerializer

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.getUserProfile, name='user-profile'),
    path('update-profile/', views.updateUserProfile, name='update-user-profile'),
    path('', views.getUsers, name='users-profiles'), 
]
