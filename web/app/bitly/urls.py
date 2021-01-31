from django.contrib import admin
from django.urls import path, re_path, include
from .view import handler404

handler404 = handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    re_path(r'^(?P<path>)/', include('front.urls')),
    path('', include('front.urls')),
]
