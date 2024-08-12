import logging

from django.utils import timezone
from rest_framework import generics, views
from rest_framework.response import Response

from reviews.models import Review, ReviewRevision, Status

from .serializers import ReviewFileSerializer, ReviewSerializer, ReviewUpdateSerializer

logger = logging.getLogger(__name__)


class ReviewListView(generics.ListAPIView):
    """
    口コミ一覧の参照
    """

    queryset = Review.objects.order_by("-reviewed_at")
    permission_classes = []
    serializer_class = ReviewSerializer


class ReviewView(generics.RetrieveAPIView):
    """
    口コミの参照
    """

    queryset = Review.objects.all()
    permission_classes = []
    serializer_class = ReviewSerializer


class ReviewCreateView(views.APIView):
    """口コミの作成

    既存の口コミの更新は行わない
    """

    def post(self, request, format=None):
        serializer = ReviewFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filename = serializer.validated_data["file".name]

        with open(filename, "wb") as f:
            f.write(serializer.validated_data["file"].read())

        # TODO:
        # df = pd.read_csv(filename)
        # for _, row in df.iterrows():
        #     pass

        return Response(status=201)


class ReviewUpdateView(generics.UpdateAPIView):
    """
    口コミの更新
    """

    queryset = Review.objects.all()
    permission_classes = []
    serializer_class = ReviewUpdateSerializer

    def update(self, request, *args, **kwargs):
        # TODO: review_revision の行追加
        # TODO: review の status, pulished_by, published_at を更新

        serializer = ReviewUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = self.get_object()

        logger.info(f"🟥 {review}")

        # update review table
        # 他のフィールドは更新厳禁
        status = serializer.validated_data["status"]
        review.status = status
        review.published_by = self.request.user if status == Status.PUBLIC else None
        review.published_at = timezone.now() if status == Status.PUBLIC else None
        review.save()

        # update review_revision table

        # TODO: 同じ detail_id のデータの is_latest を False にする
        # TODO: 行作成
        # ReviewRevision.objects.create(detail=detail, review_text=latest_review_text, revised_at=self.request.user, revised_at=timezone.now())

        # super(ReviewView, self).update(request, *args, **kwargs)
        return Response(status=201)
