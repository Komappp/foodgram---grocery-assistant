from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/recipe/<int:pk>/', views.get_recipe, name='index'),
]
