from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('menu.urls', namespace='menu')),
    path('admin/', admin.site.urls),
]
