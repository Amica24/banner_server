from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import Banner, Tag, Feature


class BannerTests(APITestCase):
    def setUp(self):
        #создаем пользователей
        user = User.objects.create_user(username="GraceCat", password="Grace123")
        admin = User.objects.create_superuser(username="admin", password="admin123")
        #создаем токены
        self.user_token = Token.objects.create(user=user)
        self.admin_token = Token.objects.create(user=admin)
        #авторизуем пользователей
        self.client_user = APIClient()
        self.client_user.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        self.client_admin = APIClient()
        self.client_admin.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        self.banner_url = reverse('user_banner')
        content = {"title": "some_title", "text": "some_text", "url": "some_url"}
        tag = Tag.objects.create(tag_id=123456)
        feature = Feature.objects.create(feature_id=78910)
        banner = Banner.objects.create(feature=feature, content=content, is_active=True)
        banner.tag.set([tag])
        content = {"title": "some_title2", "text": "some_text2", "url": "some_url2"}
        tag = Tag.objects.create(tag_id=13579)
        feature = Feature.objects.create(feature_id=24680)
        inactive_banner = Banner.objects.create(feature=feature, content=content, is_active=False)
        inactive_banner.tag.set([tag])

    def test_get_banner_with_valid_data(self):
        tag_id = 123456
        feature_id = 78910
        content = {"title": "some_title", "text": "some_text", "url": "some_url"}
        response = self.client_user.get("{}?tag_id={}&feature_id={}".format(self.banner_url, tag_id, feature_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), content)

    def test_get_banner_with_invalid_data(self):
        tag_id = 123456
        feature_id = "string"
        response = self.client_user.get("{}?tag_id={}&feature_id={}".format(self.banner_url, tag_id, feature_id))
        self.assertEqual(response.status_code, 400)

    def test_get_inactive_banner_admin(self):
        tag_id = 13579
        feature_id = 24680
        response = self.client_admin.get("{}?tag_id={}&feature_id={}".format(self.banner_url, tag_id, feature_id))
        self.assertEqual(response.status_code, 200)

    def test_get_inactive_banner_non_admin(self):
        tag_id = 13579
        feature_id = 24680
        response = self.client_user.get("{}?tag_id={}&feature_id={}".format(self.banner_url, tag_id, feature_id))
        self.assertEqual(response.status_code, 404)

