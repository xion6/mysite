from rest_framework import serializers

from reviews.models import ReviewDetail, Review, Status


class ReviewDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source="item.name")
    latest_review_text = serializers.SerializerMethodField()

    class Meta:
        model = ReviewDetail
        fields = [
            "item",
            "item_name",
            "origin_review_text",
            "latest_review_text",
            "rating",
        ]

    def get_latest_review_text(self, obj):
        return obj.latest_review_text


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

    def get_status_text(self, obj):
        return Status.choices[obj.status][1]
