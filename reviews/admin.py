from django.contrib import admin
from .models import (
    Corporation,
    Staff,
    Product,
    ReviewItem,
    Review,
    ReviewDetail,
    ReviewRevision,
)

admin.site.register(Corporation)
admin.site.register(Staff)
admin.site.register(Product)
admin.site.register(ReviewItem)
admin.site.register(Review)
admin.site.register(ReviewDetail)
admin.site.register(ReviewRevision)
