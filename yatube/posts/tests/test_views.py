from operator import attrgetter

from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Follow, Group, Post
from yatube.settings import NUM_POSTS_PER_PAGE

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='authh')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test-slug',
            description='Тестовое описание',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
            image=uploaded
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)

    def test_pages_uses_correct_template(self):
        post = PostPagesTests.post
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            (reverse('posts:group_posts', kwargs={'slug': post.group.slug})): (
                'posts/group_list.html'
            ),
            (reverse('posts:profile', kwargs={'username': post.author})): (
                'posts/profile.html'
            ),
            (reverse('posts:post_detail', kwargs={'post_id': post.id})): (
                'posts/post_detail.html'
            ),
            (reverse('posts:post_edit', kwargs={'post_id': post.id})): (
                'posts/create_post.html'
            ),
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:follow_index'): 'posts/follow.html',
        }
        for page, template in templates_pages_names.items():
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertTemplateUsed(response, template)

    def method_for_3_tests_of_post_model(self, first_object, model):
        self.assertEqual(first_object.text, model.text)
        self.assertEqual(first_object.author, model.author)
        self.assertEqual(first_object.group, model.group)
        self.assertEqual(first_object.image, model.image)

    def test_pages_show_correct_context(self):
        post = PostPagesTests.post
        pages = [
            reverse('posts:index'),
            (reverse('posts:group_posts', kwargs={'slug': post.group.slug})),
            (reverse('posts:profile', kwargs={'username': post.author})),
        ]
        for page in pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                first_object = response.context['post_list'][0]
                self.method_for_3_tests_of_post_model(first_object, post)

    def test_post_detail_page_show_correct_context(self):
        post = PostPagesTests.post
        page = reverse('posts:post_detail', kwargs={'post_id': post.id})
        response = self.authorized_client.get(page)
        first_object = response.context['post']
        self.method_for_3_tests_of_post_model(first_object, post)

    def test_edit_page_show_correct_context(self):
        post = PostPagesTests.post
        page = reverse('posts:post_edit', kwargs={'post_id': post.id})
        response = self.authorized_client.get(page)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_page_show_correct_context(self):
        page = reverse('posts:post_create')
        response = self.authorized_client.get(page)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='authh')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test-slug',
        )
        cls.LIST_SIZE = 13
        obj_list = [
            Post(
                text=f'Текст {i}',
                author=cls.user,
                group=cls.group,
                id=i,
            )
            for i in range(cls.LIST_SIZE)
        ]

        cls.post_with_id = Post.objects.bulk_create(obj_list)
        cls.sorted_objs = sorted(
            cls.post_with_id,
            key=attrgetter('id'),
            reverse=True
        )

    def setUp(self):
        self.guest_client = Client()

    def test_1st_page_contains_10_records_2nd_page_contains_3_records(self):
        pages = [
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': 'authh'})
        ]
        posts_rest = PaginatorViewsTest.LIST_SIZE - NUM_POSTS_PER_PAGE

        obj_list_1st_page = [PaginatorViewsTest.sorted_objs[i] for i in range(
            NUM_POSTS_PER_PAGE
        )]
        for page in pages:
            with self.subTest():
                response = self.guest_client.get(page)
                self.assertEqual(
                    len(response.context['page_obj']), NUM_POSTS_PER_PAGE
                )
                self.assertEqual(
                    response.context.get('page_obj').object_list[0:10],
                    obj_list_1st_page
                )
                response = self.client.get(page + '?page=2')
                self.assertEqual(len(response.context['page_obj']), posts_rest)


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='authh')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()

    def test_right_posts_show_on_pages(self):
        pages = [
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': 'authh'}),
        ]
        for page in pages:
            with self.subTest():
                response = self.guest_client.get(page)
                object = response.context.get('page_obj')[0]
                self.assertEqual(
                    object,
                    PostPagesTest.post
                )

    def test_wrong_post_show_on_right_page(self):
        self.group_2 = Group.objects.create(
            title='Test_group_2',
            slug='test-slug_2',
            description='Тестовое описание',
        )
        response = self.guest_client.get(reverse(
            'posts:group_posts',
            kwargs={'slug': 'test-slug_2'}
        ))
        object = response.context.get('page_obj').object_list
        self.assertNotIn(
            PostPagesTest.post,
            object
        )

    def get_content(self):
        response = self.guest_client.get(reverse('posts:index'))
        return response.content

    def test_cache_index(self):
        self.test_post = Post.objects.create(
            text='Кешируемый пост',
            author=PostPagesTest.user,
            group=PostPagesTest.group,
        )
        cache_content = self.get_content()
        self.test_post.delete()
        new_content = self.get_content()
        self.assertEqual(cache_content, new_content)
        cache.clear()
        new_new_content = self.get_content()
        self.assertNotEqual(cache_content, new_new_content)


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.follower = User.objects.create_user(username='reader')
        cls.following = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.following,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_follower = Client()
        self.authorized_following = Client()
        self.authorized_follower.force_login(FollowTest.follower)
        self.authorized_following.force_login(FollowTest.following)

    def test_follow(self):
        follow_count = Follow.objects.count()
        self.authorized_follower.get(
            reverse('posts:profile_follow', kwargs={
                'username': FollowTest.following.username
            })
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertTrue(
            Follow.objects.filter(
                user=FollowTest.follower,
                author=FollowTest.following
            ).exists()
        )
        self.authorized_follower.get(
            reverse('posts:profile_follow', kwargs={
                'username': FollowTest.follower.username
            })
        )
        self.assertFalse(
            Follow.objects.filter(
                user=FollowTest.follower,
                author=FollowTest.follower
            ).exists()
        )

    def test_unfollow(self):
        self.authorized_follower.get(
            reverse('posts:profile_unfollow', kwargs={
                'username': FollowTest.following.username
            })
        )
        self.assertFalse(
            Follow.objects.filter(
                user=FollowTest.follower,
                author=FollowTest.following
            ).exists()
        )

    def test_follow_posts_on_page(self):
        post_2 = Post.objects.create(
            text='Тестовый пост 2',
            author=FollowTest.follower,
            group=FollowTest.group,
        )
        Follow.objects.create(
            user=FollowTest.follower,
            author=FollowTest.following
        )
        response_1 = self.authorized_follower.get(
            reverse('posts:follow_index')
        )
        response_2 = self.authorized_following.get(
            reverse('posts:follow_index')
        )
        self.assertEqual(
            response_1.context.get('page_obj')[0],
            FollowTest.post
        )
        self.assertNotIn(
            post_2,
            response_2.context.get('page_obj').object_list
        )
