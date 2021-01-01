from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fitnessClass/', include('fitnessClass.urls')),
    path('reservations/', include('reservations.urls')),
    path('', include('accounts.urls')),
]

urlpatterns += staticfiles_urlpatterns()
