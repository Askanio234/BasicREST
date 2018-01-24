from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from postings.models import BlogPost


User = get_user_model()

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


class BlogPostAPITestCase(APITestCase):

    def setUp(self):
        user = User(username="testuser", email="test@test.com")
        user.set_password("someveryrandom")
        user.save()
        blog_post = BlogPost(user=user, title="Original",
                             content="OriginalContent")
        blog_post.save()

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = User.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("api-postings:post-create")
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {"title": "test", "content": "content"}
        url = api_reverse("api-postings:post-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        data = {"title": "test", "content": "content"}
        url = blog_post.get_api_url()
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_auth(self):
        blog_post = BlogPost.objects.first()
        data = {"title": "test", "content": "content"}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        url = blog_post.get_api_url()
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_ownership(self):
        owner = User.objects.create(username="testuser2")
        blog_post = BlogPost(user=owner, title="Test ownership",
                             content="Its important")
        blog_post.save()
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        url = blog_post.get_api_url()
        data = {"title": "test", "content": "content"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
