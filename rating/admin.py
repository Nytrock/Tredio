from django.contrib import admin

from rating.models import Review, ReviewCategory, ReviewGroup, ReviewRating


@admin.register(ReviewGroup)
class ReviewGroupAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(ReviewCategory)
class ReviewCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "review_group_id",
        "category",
        "star",
    )
    fields = (
        "review_group_id",
        "user",
        "category",
        "star",
        "content",
    )


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "review",
        "user",
        "star",
    )
    fields = (
        "review",
        "user",
        "star",
    )
