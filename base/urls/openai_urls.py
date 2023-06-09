# urls.py 

from django.urls import path
from base.views import openai_views as views


urlpatterns = [
    path('', views.getOpenAi, name='user-feelings'),
]
