from django.urls import path

from . import views


urlpatterns = [
    path("", views.ReviewListView.as_view(), name="list"),
    path("<int:pk>/", views.ReviewView.as_view(), name="detail"),
    path("create/", views.ReviewCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.ReviewUpdateView.as_view(), name="update"),
]
