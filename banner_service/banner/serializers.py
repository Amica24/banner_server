from rest_framework import serializers
from django.db import transaction

from .models import Banner, Feature, Tag


class BannerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tag_ids = serializers.ListField(required=True, write_only=True, allow_null=True)
    tag_id = serializers.SerializerMethodField()
    feature_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Feature.objects, required=True, allow_null=True, source="feature")
    content = serializers.JSONField(required=True, allow_null=True)
    is_active = serializers.BooleanField(required=True, allow_null=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Banner
        fields = ("id", "tag_id", "feature_id", "tag_ids", "content", "is_active", "created_on", "updated_on")

    def get_tag_id(self, obj):
        tags = obj.tag.all()
        list_ = []
        for tag in tags:
            list_.append(tag.tag_id)
        return list_

    def create(self, validated_data):
        with transaction.atomic():
            tags = []
            tags_ids = validated_data.pop("tag_ids")
            instance = Banner.objects.create(**validated_data)
            if tags_ids:
                for tag_id in tags_ids:
                    tag, created = Tag.objects.get_or_create(tag_id=tag_id)
                    tags.append(tag)
            instance.tag.set(tags)
            return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            tags = []
            tags_ids = validated_data.pop("tag_ids")
            if tags_ids:
                for tag_id in tags_ids:
                    tag, created = Tag.objects.get_or_create(tag_id=tag_id)
                    tags.append(tag)
                instance.tag.clear()
                instance.tag.set(tags)
            instance.tag.set(tags)
            return super().update(instance, validated_data)
