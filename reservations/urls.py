from django.urls import path
from .import views

app_name = 'reservations'

urlpatterns = [
    path('reserve/', views.reserve_view, name='reserve'),
    path('submission/', views.submission_view, name='submission')
]
