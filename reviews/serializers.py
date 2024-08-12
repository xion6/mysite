from rest_framework import serializers

from reviews.models import ReviewDetail, Review, Status

import logging

logger = logging.getLogger(__name__)


class ReviewDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source="item.name")
    latest_review_text = serializers.SerializerMethodField()

    class Meta:
        model = ReviewDetail
        fields = [
            "id",
            "item",
            "item_name",
            "review_text",
            "latest_review_text",
            "rating",
        ]
        read_only_fields = [
            "item",
            "rating",
            "review_text",
        ]

    def get_latest_review_text(self, instance):
        """最新のレビュー本文

        プロパティなのに SerializerMethodField を使わないと取得できなかった
        おそらく処理の中で別のモデルを見に行っているため
        """
        return instance.latest_review_text


class ReviewSerializer(serializers.ModelSerializer):
    review_detail = ReviewDetailSerializer(many=True, read_only=True)
    source = serializers.ReadOnlyField(source="source.name")
    mst_product = serializers.ReadOnlyField(source="mst_product.name")
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            "id",
            "source",
            "synergy_id",
            "mst_product",
            "status",
            "status_text",
            "published_by",
            "published_at",
            "reviewed_at",
            "review_detail",
        )
        read_only_fields = [
            "synergy_id",
            "mst_product",
            "reviewed_at",
            "published_by",
            "published_at",
        ]

    def get_status_text(self, instance):
        return Status.choices[instance.status][1]


class ReviewFileSerializer(serializers.Serializer):
    file = serializers.FileField()


class ReviewUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Status.choices)
