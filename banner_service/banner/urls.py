from django.urls import path, include
from rest_framework import routers

from .views import UserBannerView, BannerView

router = routers.DefaultRouter()
router.register(r'banner', BannerView, basename='Baner')

urlpatterns = [
    path('', include(router.urls)),
    path('user_banner/', UserBannerView.as_view(), name='user_banner'),
]
