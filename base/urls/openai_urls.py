# urls.py

from django.urls import path
from base.views import openai_views as views


urlpatterns = [
    path('user-emotion/', views.analyzeUserEmotions, name='user-emotions'),
    path('youtube-summarizer/', views.summarizeYoutubeVideo,
         name='youtube-summarizer'),
    path('analyze-bitcoin/', views.bitcoinPriceAnalysis,
         name='analyze-bitcoin'),
    path('generate-meal/', views.create_meals,
         name='meal-generator'),
    path('generate-image/', views.generate_image, name='generate-image')


]
