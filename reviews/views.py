from rest_framework import generics

from reviews.models import Review
from .serializers import ReviewSerializer


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.order_by("-reviewed_at")
    serializer_class = ReviewSerializer
