from django.urls import path
from . import views


urlpatterns = [

path('', views.index, name='index'),
path('create/', views.create_trophytracker, name='create_trophytracker'),
path('user_account/<int:pk>/', views.user_account_detail, name='user_account_detail'),
path('trophy_tracker/<int:pk>/', views.trophy_tracker_detail, name='trophy_tracker_detail'),
path('trophytracker/<int:pk>/update/', views.update_trophytracker, name='update_trophytracker'),
]
