import logging

from django.utils import timezone
from rest_framework import generics, views
from rest_framework.response import Response
from django.db import transaction

from reviews.models import Review, ReviewRevision, Status, Staff

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

    @transaction.atomic
    def update(self, request, *args, **kwargs):

        # if not self.request.user.is_staff:
        #     return Response(status=401)

        serializer = ReviewUpdateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=403)

        review = self.get_object()

        # reviewテーブルの更新（他のフィールドは更新厳禁）
        status = serializer.validated_data["status"]
        review.status = status
        review.published_by = self.request.user.id if status == Status.PUBLIC else None
        review.published_at = timezone.now() if status == Status.PUBLIC else None
        review.save()

        # review_revisionテーブルに行追加
        review_detail_list = serializer.validated_data["review_details"]
        for detail_dict in review_detail_list:
            detail_obj = review.review_details.get(pk=detail_dict["id"])
            latest_revision = detail_obj.review_revisions.get_latest_revision()

            # 初めての修正の場合は原本を、修正歴がある場合は修正済で最新のレビュー本文を返す
            present_review_text = (
                latest_revision.review_text
                if latest_revision
                else detail_obj.latest_review_text
            )

            # リクエストで受け取った値が現在値と異なる場合
            if not (detail_dict["latest_review_text"] == present_review_text):

                # 過去に修正履歴があれば is_latest=False にする
                if latest_revision:
                    latest_revision.is_latest = False
                    latest_revision.save()

                # 行追加
                row = {
                    "detail": detail_obj,
                    "review_text": detail_dict["latest_review_text"],
                    "rating": detail_obj.rating,
                    "revised_at": timezone.now(),
                    # TODO: self.request.user に変える
                    "revised_by": Staff.objects.get(pk=1),
                }
                ReviewRevision.objects.create(**row)

        return Response(status=201)
