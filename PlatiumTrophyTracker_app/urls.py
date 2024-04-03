from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_account/<int:pk>/', views.user_account_detail, name='user_account_detail'),
    path('trophy_tracker/<int:pk>/', views.trophy_tracker_detail, name='trophy_tracker_detail'),
    path('trophytracker/new/', views.create_trophy_tracker, name='create_trophy_tracker'),
]

 