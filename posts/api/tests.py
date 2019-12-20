from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from posts.models import Post
from django.shortcuts import reverse
from model_bakery import baker
from faker import Faker


class TestPostList(APITestCase):
    """Testing Retrieving All Posts list"""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api_all_posts")
        self.post = baker.make(Post, _quantity=3)

    def test_post_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)


class TestPostDetailAnonymously(APITestCase):
    """ Testing Post Detail API behavior for an authenticated user """

    def setUp(self):
        self.client = APIClient()
        self.post = baker.make(Post)
        self.url = reverse("api_post_detail", kwargs={"pk": self.post.id})
        self.faker = Faker()

    def test_get_post_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.post.title)
        self.assertEqual(response.data["content"], self.post.content)

    def test_update_post_detail(self):
        response = self.client.put(
            self.url,
            {"title": self.faker.sentence(), "content": self.faker.paragraph()},
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_post_detail(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)


class TestPostDetailOwnerUser(APITestCase):
    """ Testing Post Detail API behavior for the owner of the post """

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User)
        self.post = baker.make(Post, author=self.user)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("api_post_detail", kwargs={"pk": self.post.id})
        self.faker = Faker()

    def test_get_post_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["title"], self.post.title)
        self.assertEqual(response.data["content"], self.post.content)
        self.assertEqual(response.data["author"], self.user.username)
        self.assertEqual(response.status_code, 200)

    def test_update_post_detail(self):
        new_title = self.faker.sentence()
        new_content = self.faker.paragraph()
        response = self.client.put(
            self.url, {"title": new_title, "content": new_content},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], new_title)
        self.assertEqual(response.data["content"], new_content)

    def test_delete_post_detail(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TestPostDetailDifferentUser(APITestCase):
    """ Testing Post Detail API behavior for a random user post """

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User)
        self.post = baker.make(Post)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("api_post_detail", kwargs={"pk": self.post.id})
        self.faker = Faker()

    def test_get_post_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["title"], self.post.title)
        self.assertEqual(response.data["content"], self.post.content)
        self.assertEqual(response.status_code, 200)

    def test_update_post_detail(self):
        new_title = self.faker.sentence()
        new_content = self.faker.paragraph()
        response = self.client.put(
            self.url, {"title": new_title, "content": new_content},
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_post_detail(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)


class TestPostCreate(APITestCase):
    """ Testing creating posts with and without a user """

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User)
        self.url = reverse("api_create_post")
        self.faker = Faker()

    def test_create_post_anonymously(self):
        title = self.faker.sentence()
        content = self.faker.paragraph()
        with self.assertRaises(ValueError):
            self.client.post(self.url, {"title": title, "content": content})

    def test_create_post_with_user(self):
        title = self.faker.sentence()
        content = self.faker.paragraph()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {"title": title, "content": content})
        self.assertEqual(response.status_code, 201)

