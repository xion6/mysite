from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
import logging

logger = logging.getLogger(__name__)


class Corporation(models.Model):
    name = models.CharField(max_length=100)


class Staff(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)


class ReviewItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "口コミのレビュー項目"
        db_table_comment = "口コミのレビュー項目"

    def __str__(self):
        return self.name


class Status(models.IntegerChoices):
    UNCONFIRMED = 0, "未確認"
    PUBLIC = 1, "公開"
    PRIVATE = 2, "非公開"


class ReviewQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Status.PUBLIC)


class Review(models.Model):
    mst_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="保険商品マスタ"
    )
    source = models.ForeignKey(
        Corporation, on_delete=models.CASCADE, verbose_name="集計元"
    )
    synergy_id = models.CharField(max_length=100)
    reviewed_at = models.DateTimeField("レビュー回答日時", blank=True, null=True)
    status = models.IntegerField("公開ステータス", choices=Status.choices, default=0)
    published_by = models.ForeignKey(
        Staff, on_delete=models.CASCADE, verbose_name="公開者", blank=True, null=True
    )
    published_at = models.DateTimeField("公開日時", blank=True, null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    objects: ReviewQuerySet = ReviewQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "口コミ"
        db_table_comment = "口コミの基本情報"
        constraints = [
            models.UniqueConstraint(
                fields=["source", "synergy_id"], name="unique_review"
            ),
        ]
        indexes = [
            models.Index(fields=["source", "synergy_id"]),
        ]

    def __str__(self):
        return f"{self.source.name} - {self.synergy_id}"

    @property
    def published(self):
        return self.status == Status.PUBLIC


class ReviewDetail(models.Model):
    review = models.ForeignKey(
        Review, related_name="review_details", on_delete=models.CASCADE
    )
    item = models.ForeignKey(ReviewItem, on_delete=models.CASCADE)
    review_text = models.TextField("レビュー本文", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "口コミ詳細"
        db_table_comment = "各口コミの各項目に対する評価やコメントを管理（更新不可）"
        constraints = [
            models.UniqueConstraint(
                fields=["review", "item"], name="unique_review_detail"
            ),
        ]
        indexes = [
            models.Index(fields=["review", "item"]),
        ]

    def __str__(self):
        return f"{self.review.source.name} - {self.review.synergy_id} - {self.item} - {self.rating}"

    @property
    def latest_review_text(self):
        latest_revision = self.review_revisions.get_latest_revision()
        return latest_revision.review_text if latest_revision else self.review_text


class ReviewRevisionQuerySet(models.QuerySet):
    def get_latest_revision(self):
        try:
            return self.get(is_latest=True)
        except ReviewRevision.DoesNotExist:
            return None


class ReviewRevision(models.Model):
    detail = models.ForeignKey(
        ReviewDetail,
        related_name="review_revisions",
        on_delete=models.CASCADE,
        verbose_name="口コミ詳細",
    )
    review_text = models.TextField("レビュー本文", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )  # rating は修正しない
    revised_at = models.DateTimeField("修正日時", auto_now=True)
    revised_by = models.ForeignKey(
        Staff, on_delete=models.CASCADE, verbose_name="修正者"
    )
    is_latest = models.BooleanField(default=True)

    objects: ReviewRevisionQuerySet = ReviewRevisionQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "口コミ詳細の修正履歴"
        db_table_comment = "各口コミ詳細の修正履歴を管理"
        constraints = [
            models.UniqueConstraint(
                fields=["detail"],
                condition=Q(is_latest=True),
                name="unique_latest_review_revision",
            ),
        ]
