from django.urls import path
from . import views

urlpatterns = [
    path('getProducts/',views.getProducts),
    path('getProduct/<int:pk>',views.getProduct),
    path('searchProducts/<str:value>',views.searchProducts),
    path('postProducts/',views.postProducts),
    path('putProduct/<int:pk>', views.putProduct),
    path('deleteProduct/<int:pk>', views.deleteProduct),
]
