from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('api.urls')),
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('tasks/', include('tasksapp.urls')),
]