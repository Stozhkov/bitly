from django.urls import path
from . import views


urlpatterns = [
    # path('test/', views.test),
    path('<str:key>/', views.redirect_to_url),
    path('', views.main, name='main_page'),
]
