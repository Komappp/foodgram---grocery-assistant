from django.urls import path
from . import views

urlpatterns = [
    path('api/recipes/<int:pk>/', views.get_recipe, name='index'),
]
