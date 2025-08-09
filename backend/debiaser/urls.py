from django.urls import path
from .views import debias_text, get_debiased_text

urlpatterns = [
    path("debias/", debias_text, name="debias_text"),
    path('debias/get/', get_debiased_text, name="get_debiased_text"),
]