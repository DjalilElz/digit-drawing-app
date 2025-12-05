from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save-drawing/', views.save_drawing, name='save_drawing'),
]
