from django.urls import path

from . import views

urlpatterns = [
    path("", views.ReviewList.as_view(), name="reviews"),
]
