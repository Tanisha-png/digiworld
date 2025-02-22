from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('main_app.urls')), # Mounts main_app's routes at root URL
  path('accounts/', include('django.contrib.auth.urls')),
]