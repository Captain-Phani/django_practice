from django.urls import path
from . import views

urlpatterns = [
    path('login_page/',views.loginPage,name='login_page'),
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='rooms'),
    path('create_room/',views.create_room,name='roomCreation'),
    path('update_room/<str:pk>/',views.update_room,name='roomUpdation'),
    path ('delete_room/<str:pk>/',views.delete_room,name='deleteRoom')
]