from django.urls import path
from django.conf.urls import url
from Sentiment_Analysis import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('sentiment_analysis', views.sentiment_analysis, name='sentiment_analysis'),
]
