from django.urls import path
from . import views

urlpatterns = [
    path('api/cpus/', views.get_cpus, name='get_cpus'),
    path('api/motherboards/', views.get_motherboards, name='get_motherboards'),
]