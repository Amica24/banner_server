from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import Client, TestCase
from django.urls import reverse
import requests

from .models import Banner, Tag, Feature


class BannerTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="GraceCat", password="Grace123")
        user_token = Token.objects.create(user=user)
        self.user_headers = {"Authorization": "Token {}".format(user_token)}
        admin = User.objects.create_user(username="admin", password="admin123")
        admin_token = Token.objects.create(user=admin)
        self.admin_headers = {"Authorization": "Token {}".format(admin_token)}
        self.banner_url = "http://127.0.0.1:8080/user_banner/"
        tag_id = 123456
        feature_id = 78910
        content = {"title": "some_title", "text": "some_text", "url": "some_url"}
        tag = Tag.objects.create(tag_id=tag_id)
        feature = Feature.objects.create(feature_id=feature_id)
        banner = Banner.objects.create(feature=feature, content=content, is_active=True)
        banner.tag.set([tag])

    def test_get_banner_with_valid_data(self):
        tag_id = 123456
        feature_id = 78910
        content = {"title": "some_title", "text": "some_text", "url": "some_url"}
        url = reverse('user_banner')
        data = {'tag_id': tag_id, 'feature_id': feature_id}
        headers = self.user_headers
        response = requests.get("{}?tag_id={}".format(self.banner_url, tag_id), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, content)

    def test_get_banner_with_invalid_data(self):
        tag_id = 123456
        url = reverse('user_banner').
        data = {'tag_id': 'tag', 'feature_id': ["feature", ]}
        headers = self.user_headers
        response = requests.get(self.banner_url, data, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_get_inactive_banner_admin(self):
        url = reverse('user_banner')
        data = {'tag_id': 'tag', 'feature_id': ["feature", ]}
        headers = self.admin_headers
        response = requests.get(self.banner_url, data, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_get_inactive_banner_non_admin(self):
        url = reverse('user_banner')
        data = {'tag_id': 'tag', 'feature_id': ["feature", ]}
        headers = self.user_headers
        response = requests.get(self.banner_url, data, headers=headers)
        self.assertEqual(response.status_code, 400)

