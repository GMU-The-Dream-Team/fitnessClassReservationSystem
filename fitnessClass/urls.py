from django.urls import path, include
from .import views

app_name = 'fitnessClass'

urlpatterns = [
    path('schedule/', views.schedule_view, name='schedule'),
]
