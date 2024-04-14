from django.contrib import admin

from .models import Tag, Feature, Banner


class TagAdmin(admin.ModelAdmin):
    list_display = ["tag_id"]


class FeatureAdmin(admin.ModelAdmin):
    list_display = ["feature_id"]


class BannerAdmin(admin.ModelAdmin):
    list_display = [
        "id", "feature_id", "content", "is_active", "created_on", "updated_on"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Banner, BannerAdmin)
