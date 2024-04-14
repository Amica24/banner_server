import json
import os

import redis
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.views import APIView

from .models import Banner
from .serializers import UserBannerSerializer, BannerSerializer

REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_ENDPOINT = os.environ.get("REDIS_ENDPOINT")

cache = redis.Redis(host=REDIS_ENDPOINT, port=REDIS_PORT)


class UserBannerView(APIView):
    """ КЛАСС ПО ПОЛУЧЕНИЮ БАННЕРА ПОЛЬЗОВАТЕЛЯ ПО tag_id и feature_id"""
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ['get']

    def get(self, request):
        serializer = UserBannerSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse({"error": "Некорректные данные"}, status=400)
        data = serializer.data
        tag_id = data['tag_id']
        feature_id = data['feature_id']
        use_last_revision = data.get('use_last_revision', None)
        cache_key = f'banner_{tag_id}_{feature_id}'
        if use_last_revision:
            banner = get_object_or_404(
                Banner, tag__tag_id=tag_id, feature__feature_id=feature_id)
            content = banner.content
            is_active = banner.is_active
            banner = json.dumps(json.loads(serializers.serialize('json', [banner, ]))[0])
            cache.set(cache_key, banner, ex=300)
        else:
            cache_key = f'banner_{tag_id}_{feature_id}'
            banner = cache.get(cache_key)
            if not banner:
                banner = get_object_or_404(
                    Banner, tag__tag_id=tag_id, feature__feature_id=feature_id)
                content = banner.content
                is_active = banner.is_active
                banner = json.dumps(
                    json.loads(serializers.serialize('json', [banner, ]))[0])
                cache.set(cache_key, banner, ex=300)
            else:
                banner = json.loads(banner)
                content = banner["fields"]["content"]
                is_active = banner["fields"]["is_active"]
        permission_denied = not is_active and not self.request.user.is_staff
        if permission_denied:
            return JsonResponse({"error": "Баннер для не найден"}, status=404)
        return JsonResponse(content, safe=False)


class BannerView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ КЛАСС БАННЕРОВ ДЛЯ АДМИНИСТРАТОРА """
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = BannerSerializer

    def get_queryset(self):
        tag_id = self.request.query_params.get('tag_id')
        feature_id = self.request.query_params.get('feature_id')
        q = Banner.objects.all()
        if tag_id:
            q = q.filter(tag__tag_id=tag_id)
        if feature_id:
            q = q.filter(feature__feature_id=feature_id)
        return q

