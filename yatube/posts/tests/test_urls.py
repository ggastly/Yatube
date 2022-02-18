from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_static_urls(self):
        urls = {
            '/',
            '/about/author/',
            '/about/tech/',
        }
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    def test_posts_urls_exists_at_desired_location(self):
        post = PostURLTests.post
        urls = [
            '/',
            f'/group/{post.group.slug}/',
            f'/profile/{post.author}/',
            f'/posts/{post.id}/',
            '/unexisting_page/',
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                if url == '/unexisting_page/':
                    self.assertNotEqual(response.status_code, HTTPStatus.OK)
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_url__exists_at_desired_location_authorized(self):
        post = PostURLTests.post
        urls = [
            reverse('posts:post_edit', kwargs={'post_id': post.id}),
            reverse('posts:post_create'),
            reverse('posts:follow_index'),
        ]
        for url in urls:
            with self.subTest(url=url):
                response_1 = self.guest_client.get(url)
                self.assertNotEqual(response_1.status_code, HTTPStatus.OK)
                response_2 = self.authorized_client.get(url)
                self.assertEqual(response_2.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        post = PostURLTests.post
        templates_urls = {
            '/': 'posts/index.html',
            f'/group/{post.group.slug}/': 'posts/group_list.html',
            f'/profile/{post.author}/': 'posts/profile.html',
            f'/posts/{post.id}/': 'posts/post_detail.html',
            f'/posts/{post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
            '/follow/': 'posts/follow.html',
        }
        for url, template in templates_urls.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_posts_redirect_authorized(self):
        post = PostURLTests.post
        urls = [
            reverse('posts:add_comment', kwargs={'post_id': post.id}),
            reverse('posts:profile_follow', kwargs={'username': post.author}),
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': post.author}
            ),
        ]
        for url in urls:
            with self.subTest(url=url):
                response_1 = self.guest_client.get(url)
                self.assertNotEqual(response_1.status_code, HTTPStatus.OK)
                response_2 = self.authorized_client.get(url)
                self.assertEqual(response_2.status_code, HTTPStatus.FOUND)
