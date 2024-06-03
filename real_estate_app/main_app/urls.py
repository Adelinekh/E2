from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict', views.predict, name='predict'),
    path('search_history/', views.search_history, name='search_history'),
    path('search-history/clear/<int:search_id>/', views.clear_search, name='clear_search'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
