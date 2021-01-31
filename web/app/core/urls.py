from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core.views import link_list


urlpatterns = [
    path('links/', link_list)
]

urlpatterns = format_suffix_patterns(urlpatterns)
