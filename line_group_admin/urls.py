from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('select-group/', views.select_group, name='select_group'),
    path('add-new-group/', views.add_new_group, name='add_new_group'),
    path('edit-group/<int:pk>/', views.edit_group, name='edit_group'),
]
