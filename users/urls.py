from django.urls import path
from . import views

urlpatterns = [
    path('getUsers/',views.getUsers),
    path('createUser/',views.createUser),
    path('editUser/<int:pk>', views.editUser),
    path('deleteUser/<int:pk>', views.deleteUser),
]