# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('avatar/', views.avatar, name='avatar'),
    path('add_balance/', views.add_balance, name='add_balance'),
    path('buy_picture/<int:id>/', views.buy_picture, name='buy_picture'),
    
]
