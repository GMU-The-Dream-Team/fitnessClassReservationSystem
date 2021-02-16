from django.urls import path
from .import views

app_name = 'fitnessClass'

urlpatterns = [
    path('', views.schedule_view, name='schedule'),
]
