from django.urls import path
from .views import debias_text

urlpatterns = [
    path("debias/", debias_text, name="debias_text"),
]