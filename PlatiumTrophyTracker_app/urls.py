from django.urls import path
from . import views


urlpatterns = [

path('', views.index, name='index'),
path('create/', views.create_trophytracker, name='create_trophytracker'),
path('user_account/<int:pk>/', views.user_account_detail, name='user_account_detail'),

]
