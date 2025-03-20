from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path("create-room/", views.create_room, name='create_room'),
    path("update-room/<str:pk>/", views.update_room, name='update_room'),
    path("delete-room/<str:pk>/", views.delete_room, name='delete_room'),
    path("delete-message/<str:pk>/", views.delete_message, name='delete_message'), # path("delete-message/<str:pk>/<str:rPk>/", views.delete_message, name='delete_message'),
    path("login/", views.login_page, name='login'),
    path("logout/", views.logoutUser, name='logout'),
    path("register/", views.registerPage, name='register'),


]