from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_account/<int:pk>/', views.user_account_detail, name='user_account_detail'),
    path('trophy_tracker/<int:pk>/', views.trophy_tracker_detail, name='trophy_tracker_detail'),
    path('trophytracker/new/', views.create_trophy_tracker, name='create_trophy_tracker'),
    path('trophytracker/<int:pk>/update/', views.update_trophy_tracker, name='update_trophy_tracker'),
    path('trophytracker/<int:pk>/delete/', views.delete_trophy_tracker, name='delete_trophy_tracker'),
     path('trophytrackers/', views.trophy_tracker_list, name='trophy_tracker_list'),
]


 